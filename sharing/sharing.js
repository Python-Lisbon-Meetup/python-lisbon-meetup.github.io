'use strict';
const canvas = document.querySelector('#preview');
const ctx = canvas.getContext('2d');
const editor = document.querySelector('#editor');
const download = document.querySelector('#download');
const status = document.querySelector('#status');
const field = id => document.getElementById(id).value.trim();
let ready = false;
function loadImage(src) {
  return new Promise((resolve, reject) => {
    const image = new Image();
    image.onload = () => resolve(image);
    image.onerror = () => reject(new Error('Could not load artwork.'));
    image.src = src;
  });
}
// Break long words as well as normal text so every line stays inside the card.
function wrap(text, width) {
  const lines = [];
  for (const paragraph of text.split('\n')) {
    let line = '';
    for (const word of paragraph.split(/\s+/).filter(Boolean)) {
      if (line && ctx.measureText(`${line} ${word}`).width > width) {
        lines.push(line); line = '';
      }
      for (const character of (line ? ` ${word}` : word)) {
        if (line && ctx.measureText(line + character).width > width) {
          lines.push(line); line = '';
        }
        line += character;
      }
    }
    lines.push(line);
  }
  return lines;
}
function dateLabel() {
  const value = field('date');
  if (!value) return '';
  return new Date(`${value}T12:00:00`).toLocaleDateString('en-GB', { day:'numeric', month:'long', year:'numeric' });
}
let background, logo;
function render() {
  const fontScale = Number(field('font-scale')) / 100;
  const fontScaleLabel = `${Math.round(fontScale * 100)}%${fontScale === 1 ? ' (default)' : ''}`;
  document.querySelector('#font-scale-value').textContent = fontScaleLabel;
  document.querySelector('#font-scale').setAttribute('aria-valuetext', fontScaleLabel);
  if (!ready) return;
  const [width, height] = field('format').split(',').map(Number);
  canvas.width = width; canvas.height = height;
  const unit = Math.min(width, height);
  const margin = unit * .07;
  const card = {x:margin, y:margin, w:width-margin*2, h:height-margin*2};
  ctx.fillStyle = '#f5efe2'; ctx.fillRect(0,0,width,height);
  const tileSize = unit * .65;
  for (let y=0; y<height; y+=tileSize) for (let x=0; x<width; x+=tileSize) ctx.drawImage(background,x,y,tileSize,tileSize);
  ctx.fillStyle = '#fbf8f2'; ctx.fillRect(card.x,card.y,card.w,card.h);
  ctx.strokeStyle = '#1c4e94'; ctx.lineWidth = unit*.004;
  ctx.strokeRect(card.x,card.y,card.w,card.h);
  const pad = unit*.055;
  const logoSize = unit*.16;
  const corner = field('corner');
  const logoTop = corner.startsWith('top');
  const logoX = corner.endsWith('left') ? card.x+pad : card.x+card.w-pad-logoSize;
  const logoY = logoTop ? card.y+pad : card.y+card.h-pad-logoSize;
  ctx.drawImage(logo,logoX,logoY,logoSize,logoSize);
  const textX = card.x+pad;
  const textWidth = card.w-pad*2;
  const top = card.y+pad+(logoTop ? logoSize+pad*.7 : 0);
  const bottom = card.y+card.h-pad-(!logoTop ? logoSize+pad*.7 : 0);
  const sections = [
    {text:field('title'),size:unit*.066,weight:700,color:'#123566',gap:unit*.033},
    {text:[dateLabel(),field('time')].filter(Boolean).join(' · '),size:unit*.033,weight:600,color:'#1c4e94',gap:unit*.016},
    {text:field('location'),size:unit*.036,weight:600,color:'#1c4e94',gap:unit*.032},
    {text:field('description'),size:unit*.029,weight:400,color:'#13294b',gap:0}
  ].filter(section => section.text);
  let layout;
  // Shrink the whole text block together when details need more room.
  for (let scale=fontScale; scale>=.1; scale-=.01) {
    layout = sections.map(section => {
      const size=section.size*scale;
      ctx.font=`${section.weight} ${size}px Rubik`;
      return {...section,size,lines:wrap(section.text,textWidth),lineHeight:size*1.3,gap:section.gap*scale};
    });
    if (layout.reduce((sum,s)=>sum+s.lines.length*s.lineHeight+s.gap,0)<=bottom-top) break;
  }
  ctx.textBaseline='top';
  let y=top;
  for (const section of layout) {
    ctx.font=`${section.weight} ${section.size}px Rubik`; ctx.fillStyle=section.color;
    for (const line of section.lines) {ctx.fillText(line,textX,y); y+=section.lineHeight;}
    y+=section.gap;
  }
  document.querySelector('#dimensions').textContent=`${width} × ${height} px`;
  canvas.setAttribute('aria-label',`Event image: ${sections.map(s=>s.text).join('. ')}`);
}
editor.addEventListener('submit', event => event.preventDefault());
editor.addEventListener('input',render);
editor.addEventListener('change',render);
download.addEventListener('click', () => {
  download.disabled=true;
  canvas.toBlob(blob => {
    download.disabled=false;
    if (!blob) {status.textContent='The image could not be exported. Please try again.';return;}
    const url=URL.createObjectURL(blob);
    const link=document.createElement('a');
    link.download=`python-lisbon-${field('date') || 'event'}-${canvas.width}x${canvas.height}.png`;
    link.href=url; document.body.append(link); link.click(); link.remove();
    setTimeout(()=>URL.revokeObjectURL(url),10000);
    status.textContent='PNG ready. Your download has started.';
  },'image/png');
});
Promise.all([
  loadImage('/assets/pattern.webp'),loadImage('/assets/tiles/snakes-medallion.webp'),
  ...[400,600,700].map(weight=>document.fonts.load(`${weight} 24px Rubik`))
]).then(([pattern,medallion]) => {
  background=pattern; logo=medallion; ready=true; render(); download.disabled=false;
  status.textContent='Ready to share. PNG downloads at the full resolution shown above.';
}).catch(() => {status.textContent='Unable to load the artwork or fonts. Please refresh to try again.';});
