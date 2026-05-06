const {Jimp} = require('jimp');

async function run() {
  const img = await Jimp.read('/srv/code/david/workspace/Parling-Academy/logo.png');
  const w = img.width, h = img.height;

  // Sample bg from corners
  const samples = [[2,2],[w-3,2],[2,h-3],[w-3,h-3]];
  let avgR=0, avgG=0, avgB=0;
  samples.forEach(([x,y]) => {
    const c = img.getPixelColor(x,y);
    avgR += (c>>>24)&0xff; avgG += (c>>>16)&0xff; avgB += (c>>>8)&0xff;
  });
  avgR=avgR/4|0; avgG=avgG/4|0; avgB=avgB/4|0;
  console.log('BG:', avgR, avgG, avgB);

  const TOLERANCE = 55;
  let removed = 0;

  for (let y = 0; y < h; y++) {
    for (let x = 0; x < w; x++) {
      const c = img.getPixelColor(x, y);
      const r=(c>>>24)&0xff, g=(c>>>16)&0xff, b=(c>>>8)&0xff;
      const dist = Math.sqrt((r-avgR)**2+(g-avgG)**2+(b-avgB)**2);
      if (dist < TOLERANCE) {
        img.setPixelColor(0x00000000, x, y);
        removed++;
      }
    }
  }
  console.log('removed:', removed, 'kept:', w*h - removed);
  await img.write('/srv/code/david/workspace/Parling-Academy/logo-nobg.png');
  console.log('done');
}
run().catch(console.error);
