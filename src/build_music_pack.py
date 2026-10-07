from pathlib import Path
import argparse,hashlib,json,math,re,subprocess,sys,tempfile,uuid,wave,shutil
p=argparse.ArgumentParser(description='Build an independent Vehicle Radio music-pack addon.')
p.add_argument('--id',required=True)
p.add_argument('--name',required=True)
p.add_argument('--input',required=True,type=Path)
p.add_argument('--output',required=True,type=Path)
p.add_argument('--ffmpeg',default=shutil.which('ffmpeg') or 'ffmpeg')
a=p.parse_args()
if not re.fullmatch(r'[A-Za-z0-9_]+',a.id):p.error('Use only letters, digits and underscores for --id')
if not a.name.isascii():p.error('Use an ASCII display name for the debug HUD font.')
files=sorted(f for f in a.input.iterdir()if f.suffix.lower()in {'.wav','.mp3','.ogg','.flac','.m4a'} and f.is_file())
if not files:p.error('Input folder contains no supported audio files')
tracks=[];seen=set()
with tempfile.TemporaryDirectory(prefix='vehicle-radio-pack-')as work:
    for i,f in enumerate(files):
        converted=Path(work)/f'{i}.wav'
        print('Converting: '+f.name,flush=True)
        result=subprocess.run([str(a.ffmpeg),'-y','-hide_banner','-loglevel','error','-i',str(f),'-ar','22050','-ac','1','-c:a','pcm_s16le',str(converted)],capture_output=True,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        if result.returncode:raise RuntimeError(f.name+': '+result.stderr.decode('utf8',errors='replace'))
        raw=converted.read_bytes()
        digest=hashlib.sha256(raw).hexdigest()[:24]
        if digest in seen:continue
        seen.add(digest)
        with wave.open(str(converted),'rb')as w:
            assert w.getsampwidth()==2 and w.getnchannels()==1
            duration=math.ceil(w.getnframes()*1000/w.getframerate())
        encoded=raw.hex()
        chunks=[encoded[j:j+8192]for j in range(0,len(encoded),8192)]
        tracks.append('{id='+json.dumps(digest)+',duration_ms='+str(duration)+',size='+str(len(raw))+',chunks={'+','.join("'"+c+"'"for c in chunks)+'}}')
    resource='mods/vehicle_radio_packs/'+a.id
    source='-- HD2-Addon: '+resource+'\nlocal pack={id='+json.dumps(a.id)+',name='+json.dumps(a.name)+',tracks={'+','.join(tracks)+'}}\n'+'''
local radio=rawget(_G,'VehicleRadio')
if radio and radio.api==1 then
 local ok,why=radio.register_pack(pack)
 if not ok then error('Vehicle Radio pack rejected: '..tostring(why))end
else
 local pending=rawget(_G,'VehicleRadioPending')
 if not pending then pending={};rawset(_G,'VehicleRadioPending',pending)end
 pending[#pending+1]=pack
end
return true
'''
    entry=Path(work)/'music_pack.lua';entry.write_bytes(source.encode())
    try:
        from lupa.luajit21 import LuaRuntime
    except ImportError:
        pass
    else:
        LuaRuntime().eval('function(s)assert(loadstring(s))end')(source)
    sys.path.insert(0,str(Path(__file__).resolve().parent))
    import build_addon
    a.output.parent.mkdir(parents=True,exist_ok=True)
    build_addon.build_package(resource,str(entry),str(uuid.uuid5(uuid.NAMESPACE_URL,resource)),str(a.output),a.name+' - Vehicle Radio Pack',description='')
print(a.output)
