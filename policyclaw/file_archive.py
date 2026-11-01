#!/usr/bin/env python3
import argparse
import base64
import builtins
from collections import Counter
from concurrent.futures import ThreadPoolExecutor
from contextlib import closing
from datetime import datetime, timezone
import fnmatch
import hashlib
import io
import json
import os
from pathlib import Path, PurePosixPath
import re
import sqlite3
import stat
from itertools import islice
import zlib

SUFFIX = '.archive.sqlite'
FORMAT = 'lossless-sqlite-files-v1'

def sha(data):
    return hashlib.sha256(data).hexdigest()

def safe(path):
    p = PurePosixPath(path)
    if p.is_absolute() or '..' in p.parts or str(p) != path:
        raise ValueError(f'Unsafe archive path: {path!r}')
    return p

def attrs(path):
    return {n:base64.b64encode(os.getxattr(path,n,follow_symlinks=False)).decode('ascii')
            for n in sorted(os.listxattr(path,follow_symlinks=False))}

def walk(root):
    yield Path(root)
    for base, dirs, files in os.walk(root,followlinks=False):
        dirs.sort(); files.sort()
        for n in dirs + files:
            yield Path(base)/n

def identity(s):
    return (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_mode,s.st_nlink)

def record(root,path):
    s=path.lstat()
    kind='directory' if stat.S_ISDIR(s.st_mode) else 'file' if stat.S_ISREG(s.st_mode) else 'symlink' if stat.S_ISLNK(s.st_mode) else None
    if kind is None: raise ValueError(f'Unsupported special file: {path}')
    meta={k:getattr(s,'st_'+k) for k in ('dev','ino','mode','uid','gid','size','nlink','atime_ns','mtime_ns','ctime_ns')}
    meta['xattrs']=attrs(path)
    meta['link_target']=os.readlink(path) if kind=='symlink' else None
    data=path.read_bytes() if kind=='file' else None
    if identity(s)!=identity(path.lstat()): raise RuntimeError(f'Source changed during read: {path}')
    return (path.relative_to(root).as_posix(),kind,sha(data) if data is not None else None,
            zlib.compress(data) if data is not None else None,json.dumps(meta,separators=(',',':')))

def connect_ro(database):
    return sqlite3.connect(Path(database).absolute().as_uri()+'?mode=ro&immutable=1',uri=True)

class Archive:
    def __init__(self,database):
        self.database=Path(database).absolute()
        with closing(connect_ro(self.database)) as c:
            self.manifest=json.loads(c.execute('SELECT value FROM info WHERE key=?',('manifest',)).fetchone()[0])
        if self.manifest['format']!=FORMAT:raise ValueError('Unsupported archive format')
    def rows(self,prefix=None,payload=False):
        fields='path,kind,sha256,payload,metadata' if payload else 'path,kind,sha256,NULL,metadata'
        query='SELECT '+fields+' FROM entries';args=()
        if prefix is not None and prefix!='.':
            prefix=str(safe(prefix));query+=' WHERE path=? OR (path>=? AND path<?)';args=(prefix,prefix+'/',prefix+'0')
        with closing(connect_ro(self.database)) as c:
            for row in c.execute(query+' ORDER BY path',args):yield row
    def resolve_path(self,path):
        path=str(safe(str(path)))
        for _ in range(40):
            with closing(connect_ro(self.database)) as c:
                row=c.execute('SELECT kind,metadata FROM entries WHERE path=?',(path,)).fetchone()
                if row and row[0]!='symlink':return path
                parts=PurePosixPath(path).parts
                found=None
                for n in range(1,len(parts)+1):
                    parent=PurePosixPath(*parts[:n]).as_posix()
                    r=c.execute('SELECT kind,metadata FROM entries WHERE path=?',(parent,)).fetchone()
                    if r and r[0]=='symlink':found=(parent,json.loads(r[1])['link_target'],parts[n:]);break
            if found is None:return path
            parent,target,tail=found
            logical=Path(self.manifest['source'])
            absolute=Path(os.path.normpath(str((logical/parent).parent/target/Path(*tail))))
            if not absolute.is_relative_to(logical):return absolute
            path=absolute.relative_to(logical).as_posix()
        raise OSError('Too many archived symlinks')
    def paths(self,prefix=None):
        resolved=self.resolve_path(prefix) if prefix is not None else None
        if isinstance(resolved,Path):
            if resolved.is_dir():
                yield str(prefix)
                for p in walk(resolved):
                    if p!=resolved:yield (PurePosixPath(prefix)/p.relative_to(resolved)).as_posix()
            return
        for r in self.rows(resolved):
            yield r[0] if resolved==prefix or prefix is None else (PurePosixPath(prefix)/PurePosixPath(r[0]).relative_to(resolved)).as_posix()
    def kind(self,path):
        path=self.resolve_path(path)
        if isinstance(path,Path):return 'directory' if path.is_dir() else 'file' if path.is_file() else None
        with closing(connect_ro(self.database)) as c:
            r=c.execute('SELECT kind FROM entries WHERE path=?',(str(path),)).fetchone()
        return r[0] if r else None
    def read_bytes(self,path):
        resolved=self.resolve_path(path)
        if isinstance(resolved,Path):return read_bytes(resolved)
        if resolved!=str(path):
            overlay=Path(self.manifest['source'])/resolved
            if overlay.exists():return overlay.read_bytes()
        with closing(connect_ro(self.database)) as c:
            r=c.execute('SELECT kind,sha256,payload FROM entries WHERE path=?',(str(resolved),)).fetchone()
        if not r:raise FileNotFoundError(path)
        if r[0]!='file':raise IsADirectoryError(path)
        data=zlib.decompress(r[2])
        if sha(data)!=r[1]:raise ValueError(f'Payload checksum mismatch: {path}')
        return data
    def verify(self,source=None,restored=False):
        source=Path(source).absolute() if source is not None else None
        paths=set();inodes=Counter();nlinks={};counts=Counter();byte_count=0;restored_groups={};actual_groups={}
        with closing(connect_ro(self.database)) as c:
            if c.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise ValueError('SQLite integrity check failed')
            if c.execute('SELECT count(*) FROM entries').fetchone()[0]!=self.manifest['entries']:raise ValueError('Entry count mismatch')
        def check(row):
            path,kind,checksum,payload,metadata=row;safe(path);m=json.loads(metadata)
            if kind not in ('directory','file','symlink'):raise ValueError('Invalid kind')
            data=zlib.decompress(payload) if kind=='file' else None
            if kind=='file' and (sha(data)!=checksum or len(data)!=m['size']):raise ValueError(f'Payload checksum mismatch: {path}')
            actual_inode=None
            if source is not None:
                p=source/path;s=p.lstat();actual_inode=(s.st_dev,s.st_ino)
                keys=('mode','uid','gid','mtime_ns') if restored else ('dev','ino','mode','uid','gid','size','nlink','mtime_ns')
                if any(getattr(s,'st_'+k)!=m[k] for k in keys):raise ValueError(f'Source metadata changed: {path}')
                if attrs(p)!=m['xattrs']:raise ValueError(f'Source xattrs changed: {path}')
                if kind=='file' and sha(p.read_bytes())!=checksum:raise ValueError(f'Source bytes changed: {path}')
                if kind=='symlink' and os.readlink(p)!=m['link_target']:raise ValueError(f'Source link changed: {path}')
                if identity(s)!=identity(p.lstat()):raise ValueError(f'Source changed during verification: {path}')
            return path,kind,m,actual_inode
        with ThreadPoolExecutor(max_workers=32) as ex:
            it=iter(self.rows(payload=True))
            while batch:=list(islice(it,128)):
                for path,kind,m,actual_inode in ex.map(check,batch):
                    paths.add(path);counts[kind]+=1
                    if kind=='file':
                        byte_count+=m['size'];key=(m['dev'],m['ino']);inodes[key]+=1;nlinks[key]=m['nlink']
                        if restored:
                            if restored_groups.setdefault(key,actual_inode)!=actual_inode or actual_groups.setdefault(actual_inode,key)!=key:raise ValueError('Restored hardlink topology mismatch')
        if '.' not in paths or self.kind('.')!='directory':raise ValueError('Missing root')
        for path in paths:
            if path!='.' and str(PurePosixPath(path).parent) not in paths:raise ValueError(f'Missing parent: {path}')
        if source is not None and {p.relative_to(source).as_posix() for p in walk(source)}!=paths:raise ValueError('Source file set changed')
        external={k:v for k,v in inodes.items() if v<nlinks[k]}
        return {'database':str(self.database),'entries':len(paths),'counts':dict(counts),'source_bytes':byte_count,
                'source_compared':source is not None,'restored_source':restored,'internal_hardlink_extra_entries':sum(v-1 for v in inodes.values()),
                'external_hardlink_groups':len(external),'external_hardlink_entries':sum(external.values()),
                'verified_utc':datetime.now(timezone.utc).isoformat()}
    def restore(self,destination,prefix='.'):
        destination=Path(destination).absolute();safe(prefix)
        if destination.exists():raise FileExistsError(destination)
        selected=list(self.rows(prefix));metadata={r[0]:(r[1],json.loads(r[4])) for r in selected}
        if prefix not in metadata or metadata[prefix][0]!='directory':raise ValueError('Restore prefix must be directory')
        for path,(kind,m) in metadata.items():
            safe(path)
            if path!=prefix and metadata.get(str(PurePosixPath(path).parent),(None,None))[0]!='directory':raise ValueError('Invalid parent')
        destination.mkdir(mode=0o700);links={}
        def target(path):return destination if path==prefix else destination/PurePosixPath(path).relative_to(prefix)
        for path,(kind,m) in sorted(metadata.items(),key=lambda x:len(PurePosixPath(x[0]).parts)):
            if path==prefix:continue
            p=target(path)
            if kind=='directory':p.mkdir(mode=0o700)
            elif kind=='symlink':os.symlink(m['link_target'],p)
            elif kind=='file':
                key=(m['dev'],m['ino'])
                if key in links:os.link(links[key],p)
                else:p.write_bytes(self.read_bytes(path));links[key]=p
        for path,(kind,m) in sorted(metadata.items(),key=lambda x:len(PurePosixPath(x[0]).parts),reverse=True):
            p=target(path);s=p.lstat()
            if (s.st_uid,s.st_gid)!=(m['uid'],m['gid']):os.chown(p,m['uid'],m['gid'],follow_symlinks=False)
            if kind!='symlink':os.chmod(p,stat.S_IMODE(m['mode']))
            current=attrs(p)
            for n,v in m['xattrs'].items():
                if current.get(n)!=v:os.setxattr(p,n,base64.b64decode(v),follow_symlinks=False)
            os.utime(p,ns=(m['atime_ns'],m['mtime_ns']),follow_symlinks=False)
        return str(destination)

def pack(source,database):
    source=Path(source).absolute();database=Path(database).absolute()
    if database.exists():raise FileExistsError(database)
    counts=Counter();total=0;n=0
    fd=os.open(database,os.O_CREAT|os.O_EXCL|os.O_WRONLY,0o600);os.close(fd)
    try:
        with closing(sqlite3.connect(database)) as c,ThreadPoolExecutor(max_workers=32) as ex:
            c.execute('PRAGMA journal_mode=OFF');c.execute('PRAGMA synchronous=OFF')
            c.execute('CREATE TABLE entries(path TEXT PRIMARY KEY,kind TEXT NOT NULL,sha256 TEXT,payload BLOB,metadata TEXT NOT NULL)')
            c.execute('CREATE TABLE info(key TEXT PRIMARY KEY,value TEXT NOT NULL) WITHOUT ROWID')
            it=iter(walk(source))
            while batch:=list(islice(it,128)):
                rows=list(ex.map(lambda p:record(source,p),batch));c.executemany('INSERT INTO entries VALUES(?,?,?,?,?)',rows)
                for r in rows:
                    n+=1;counts[r[1]]+=1
                    if r[1]=='file':total+=json.loads(r[4])['size']
                if n%8192<128:print(json.dumps({'entries':n,'source_bytes':total}),flush=True)
            result={'format':FORMAT,'source':str(source),'entries':n,'counts':dict(counts),'source_bytes':total,'created_utc':datetime.now(timezone.utc).isoformat()}
            c.execute('INSERT INTO info VALUES(?,?)',('manifest',json.dumps(result)));c.commit()
            if c.execute('PRAGMA integrity_check').fetchone()[0]!='ok':raise ValueError('SQLite integrity check failed')
        return result
    except BaseException:
        raise

_ARCHIVES={}
def archived_path(path):
    path=Path(path).absolute()
    for root,archive in tuple(_ARCHIVES.items()):
        if path.is_relative_to(root):return archive,path.relative_to(root).as_posix()
    for parent in (path,*path.parents):
        if not parent.name:continue
        db=parent.with_name(parent.name+SUFFIX)
        if db.is_file():
            a=_ARCHIVES.setdefault(parent,Archive(db));return a,path.relative_to(parent).as_posix()
    return None,None

def exists(path):
    if Path(path).exists():return True
    a,p=archived_path(path);return bool(a and a.kind(p))
def is_file(path):
    if Path(path).exists():return Path(path).is_file()
    a,p=archived_path(path);return bool(a and a.kind(p)=='file')
def is_dir(path):
    if Path(path).exists():return Path(path).is_dir()
    a,p=archived_path(path);return bool(a and a.kind(p)=='directory')
def read_bytes(path):
    if Path(path).exists():return Path(path).read_bytes()
    a,p=archived_path(path)
    if a is None:raise FileNotFoundError(path)
    return a.read_bytes(p)
def read_text(path,encoding='utf-8',errors='strict'):
    return read_bytes(path).decode(encoding,errors)
def open_file(path,mode='r',buffering=-1,encoding=None,errors=None,newline=None):
    path=Path(path)
    if not path.exists() and ('a' in mode or '+' in mode or 'x' in mode):
        archive,relative=archived_path(path)
        if archive and archive.kind(relative):
            if 'x' in mode:raise FileExistsError(path)
            if 'w' not in mode:
                path.parent.mkdir(parents=True,exist_ok=True)
                path.write_bytes(archive.read_bytes(relative))
    if path.exists() or any(c in mode for c in 'wax+'):
        return builtins.open(path,mode,buffering=buffering,encoding=encoding,errors=errors,newline=newline)
    if 'r' not in mode:raise ValueError(f'Unsupported mode: {mode}')
    raw=io.BytesIO(read_bytes(path))
    return raw if 'b' in mode else io.TextIOWrapper(raw,encoding=encoding or 'utf-8',errors=errors,newline=newline)
def copytree(source,destination,**kwargs):
    import shutil
    archive,relative=archived_path(source)
    if archive is None:return shutil.copytree(source,destination,**kwargs)
    source=Path(source);destination=Path(destination)
    destination.mkdir(parents=True,exist_ok=kwargs.get('dirs_exist_ok',False))
    for path in rglob(source,'*'):
        target=destination/path.relative_to(source)
        if is_dir(path):target.mkdir(exist_ok=True)
        else:
            target.parent.mkdir(parents=True,exist_ok=True)
            copy2(path,target)
    return str(destination)

def stat_file(path,*,follow_symlinks=True):
    if Path(path).exists():return Path(path).stat(follow_symlinks=follow_symlinks)
    archive,relative=archived_path(path)
    if archive is None:raise FileNotFoundError(path)
    resolved=archive.resolve_path(relative) if follow_symlinks else relative
    if isinstance(resolved,Path):return resolved.stat(follow_symlinks=follow_symlinks)
    row=next((r for r in archive.rows(resolved) if r[0]==resolved),None)
    if row is None:raise FileNotFoundError(path)
    from types import SimpleNamespace
    m=json.loads(row[4]);values={'st_'+k:v for k,v in m.items() if k not in ('xattrs','link_target')}
    for key in ('atime','mtime','ctime'):values['st_'+key]=m.get(key+'_ns',0)/1e9
    return SimpleNamespace(**values)

def copy2(source,destination,*,follow_symlinks=True):
    import shutil
    if Path(source).exists():return shutil.copy2(source,destination,follow_symlinks=follow_symlinks)
    destination=Path(destination)
    if destination.is_dir():destination/=Path(source).name
    archive,relative=archived_path(source)
    if archive is None:raise FileNotFoundError(source)
    resolved=archive.resolve_path(relative)
    if isinstance(resolved,Path):return shutil.copy2(resolved,destination,follow_symlinks=follow_symlinks)
    row=next(r for r in archive.rows(resolved) if r[0]==resolved);m=json.loads(row[4])
    destination.write_bytes(archive.read_bytes(relative));os.chmod(destination,stat.S_IMODE(m['mode']))
    for n,v in m['xattrs'].items():os.setxattr(destination,n,base64.b64decode(v),follow_symlinks=False)
    os.utime(destination,ns=(m['atime_ns'],m['mtime_ns']))
    return str(destination)

def _matches(relative,pattern):
    def match(parts,patterns):
        if not patterns:return not parts
        if patterns[0]=='**':return any(match(parts[i:],patterns[1:]) for i in range(len(parts)+1))
        return bool(parts) and fnmatch.fnmatchcase(parts[0],patterns[0]) and match(parts[1:],patterns[1:])
    return match(relative.split('/'),pattern.split('/'))

def glob(root,pattern):
    root=Path(root);found=set(root.glob(pattern)) if root.exists() else set()
    a,p=archived_path(root)
    if a:
        prefix='' if p=='.' else p+'/'
        for path in a.paths(p):
            if path==p:continue
            relative=path.removeprefix(prefix)
            if relative!='.' and _matches(relative,pattern):found.add(root/relative)
    return iter(sorted(found))
def rglob(root,pattern):return glob(root,'**/'+pattern)
def iterdir(root):
    if not is_dir(root):
        if not exists(root):raise FileNotFoundError(root)
        raise NotADirectoryError(root)
    return glob(root,'*')
def listdir(root='.'):
    return [p.name for p in iterdir(root)]

def seed_cache(source,destination,no_clobber=False):
    import shutil
    source=Path(source).absolute();destination=Path(destination).absolute()
    if source==destination:raise ValueError('Source and destination cache must differ')
    if not is_dir(source):raise FileNotFoundError(source)
    source_db=source.with_name(source.name+SUFFIX);destination_db=destination.with_name(destination.name+SUFFIX)
    if source_db.is_file() and not destination.exists() and not destination_db.exists():
        destination.parent.mkdir(parents=True,exist_ok=True)
        temporary=destination_db.with_name(destination_db.name+'.tmp.'+str(os.getpid()))
        shutil.copy2(source_db,temporary);os.replace(temporary,destination_db)
        if source.exists():shutil.copytree(source,destination,dirs_exist_ok=True)
        return str(destination)
    destination.mkdir(parents=True,exist_ok=True)
    for path in rglob(source,'*'):
        target=destination/path.relative_to(source)
        if is_dir(path):continue
        if exists(target) and (no_clobber or read_bytes(target)==read_bytes(path)):continue
        target.parent.mkdir(parents=True,exist_ok=True);copy2(path,target)
    return str(destination)

if __name__=='__main__':
    ap=argparse.ArgumentParser(description=__doc__);sp=ap.add_subparsers(dest='command',required=True)
    p=sp.add_parser('pack');p.add_argument('source',type=Path);p.add_argument('database',type=Path)
    p=sp.add_parser('verify');p.add_argument('database',type=Path);p.add_argument('--source',type=Path);p.add_argument('--restored-source',type=Path)
    p=sp.add_parser('restore');p.add_argument('database',type=Path);p.add_argument('destination',type=Path);p.add_argument('--prefix',default='.')
    p=sp.add_parser('seed-cache');p.add_argument('source',type=Path);p.add_argument('destination',type=Path);p.add_argument('--no-clobber',action='store_true')
    args=ap.parse_args()
    if args.command=='pack':result=pack(args.source,args.database)
    elif args.command=='seed-cache':result=seed_cache(args.source,args.destination,args.no_clobber)
    elif args.command=='verify':result=Archive(args.database).verify(args.restored_source or args.source,restored=args.restored_source is not None)
    else:result=Archive(args.database).restore(args.destination,args.prefix)
    print(json.dumps(result,indent=2))
