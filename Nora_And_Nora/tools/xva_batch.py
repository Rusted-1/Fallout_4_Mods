"""Turn a voice sheet CSV into an xVASynth batch CSV.
Usage: python3 -I xva_batch.py <voice sheet.csv> <out batch.csv> [<voice id for both Noras, e.g. f4_nora>] [<plugin name>]
Columns (from xVASynth javascript/batch.js): game_id, voice_id, text, vocoder, out_path, pacing, pitch_amp.
voice_id is a placeholder per speaker; replace it with the model's voice ID in xVASynth.
out_path ends in the final file name, so each line is written straight into the game folder layout."""
import sys,csv
src,out=sys.argv[1:3]
ONE_VOICE=sys.argv[3] if len(sys.argv)>3 else None
PLUGIN=sys.argv[4] if len(sys.argv)>4 else 'NoraAndNora.esp'
VOICE={'Organic Nora':'VOICE_ID_ORGANIC_NORA','Synth Nora':'VOICE_ID_SYNTH_NORA'}
PITCH={'neutral':1.0,'sad':0.9,'happy':1.15,'surprise':1.15,'fear':1.2,'angry':1.2}   # pitch variation; xVASynth has no emotion column in batch

rows=list(csv.DictReader(open(src,encoding='utf-8-sig')))
FOLDER='Nora and Nora/Sound/Voice/%s/PlayerVoiceFemale01/'%PLUGIN
with open(out,'w',newline='',encoding='utf-8') as f:            # no BOM: xVASynth reads the header literally
    w=csv.writer(f,quoting=csv.QUOTE_MINIMAL,lineterminator='\n')
    w.writerow(['game_id','voice_id','text','vocoder','out_path','pacing','pitch_amp'])
    for r in rows:
        w.writerow(['fallout4',ONE_VOICE or VOICE[r['Speaker']],r['Text'],'',FOLDER+r['File name'],1.0,PITCH.get(r['Emotion'],1.0)])
print(len(rows),'rows')
