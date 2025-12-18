import express from 'express';
import cors from 'cors';
import dotenv from 'dotenv';
import OpenAI from 'openai';
import { createClient } from '@supabase/supabase-js';

dotenv.config();

const PORT = process.env.PORT || 3001;
const app = express();
app.use(cors());

const openaiApiKey = process.env.OPENAI_API_KEY;
if (!openaiApiKey) {
  console.warn('OPENAI_API_KEY not set in environment; /api/video will fail');
}
const openai = new OpenAI({ apiKey: openaiApiKey });

const SUPABASE_URL = process.env.SUPABASE_URL;
const SUPABASE_ANON_KEY = process.env.SUPABASE_ANON_KEY;
let supabase = null;
if (SUPABASE_URL && SUPABASE_ANON_KEY) {
  supabase = createClient(SUPABASE_URL, SUPABASE_ANON_KEY);
} else {
  console.warn('SUPABASE_URL or SUPABASE_ANON_KEY not set; /api/video-id will fail');
}

app.get('/api/video-id', async (req, res) => {
  try {
    if (!supabase) return res.status(500).json({ error: 'supabase not configured' });
    const { data, error } = await supabase.from('test').select('video').eq('id', 2).limit(1);
    if (error) {
      console.error('supabase error', error);
      return res.status(500).json({ error: 'supabase error' });
    }
    if (!data || data.length === 0) return res.status(404).json({ error: 'no video found' });
    // sanitize the video id (trim and remove stray whitespace/newlines)
    const raw = data[0].video ?? '';
    const videoId = String(raw).trim().replace(/\s+/g, '');
    return res.json({ videoId });
  } catch (err) {
    console.error(err);
    res.status(500).json({ error: 'unexpected error' });
  }
});

app.get('/api/video/:id', async (req, res) => {
  const id = req.params.id;
  if (!openaiApiKey) return res.status(500).json({ error: 'openai api key not configured' });
  try {
    // sanitize incoming id param to remove whitespace/newlines that may have been stored
    const cleanId = String(id).trim().replace(/\s+/g, '');
    const content = await openai.videos.downloadContent(cleanId);
    const arrayBuffer = await content.arrayBuffer();
    const buffer = Buffer.from(arrayBuffer);
    res.setHeader('Content-Type', 'video/mp4');
    res.setHeader('Content-Length', buffer.length);
    res.send(buffer);
  } catch (err) {
    console.error('error downloading video content', err);
    res.status(500).json({ error: 'failed to download video' });
  }
});

app.listen(PORT, () => {
  console.log(`Video proxy server listening on http://localhost:${PORT}`);
});
