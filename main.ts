// news-image-20261124 entry (Node 22, standard library only).
//
// The entry is the PNG drawn by draw_image.py and stored beside this file
// as entry.png. This program checks that the file is a well-formed PNG
// inside the competition's limits, then places a copy at
// $MAKEFUN_OUTPUT_DIR/entry.png (or /output/entry.png when that variable
// is unset). It writes nothing else, so two runs produce identical bytes.

import { chmodSync, copyFileSync, mkdirSync, readFileSync, statSync } from 'node:fs';
import { join } from 'node:path';

const MAX_BYTES = 1024 * 1024;
const MAX_SIDE = 1024;
const PNG_MAGIC = Buffer.from([0x89, 0x50, 0x4e, 0x47, 0x0d, 0x0a, 0x1a, 0x0a]);

const source = new URL('./entry.png', import.meta.url);
const bytes = readFileSync(source);

if (bytes.length > MAX_BYTES) {
  throw new Error(`entry.png is ${bytes.length} bytes, over the ${MAX_BYTES} byte limit`);
}
if (!bytes.subarray(0, 8).equals(PNG_MAGIC)) {
  throw new Error('entry.png does not start with the PNG signature');
}
// Width and height live in the IHDR chunk: 8-byte signature, 4-byte length,
// 4-byte type "IHDR", then width and height as 4-byte big-endian integers.
const ihdrType = bytes.subarray(12, 16).toString('latin1');
if (ihdrType !== 'IHDR') {
  throw new Error(`first PNG chunk is ${ihdrType}, expected IHDR`);
}
const width = bytes.readUInt32BE(16);
const height = bytes.readUInt32BE(20);
if (width === 0 || height === 0 || width > MAX_SIDE || height > MAX_SIDE) {
  throw new Error(`image is ${width}x${height}, over the ${MAX_SIDE}x${MAX_SIDE} limit`);
}

const outDir = process.env.MAKEFUN_OUTPUT_DIR ?? '/output';
mkdirSync(outDir, { recursive: true });
const target = join(outDir, 'entry.png');
copyFileSync(source, target);
chmodSync(target, 0o644);

const written = statSync(target);
console.log(`entry.png: ${width}x${height}, ${written.size} bytes -> ${target}`);
