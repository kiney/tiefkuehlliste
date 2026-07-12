export function formatQuantity(parts){return parts.map(p=>p.kind==='package'?`${p.amount} × ${p.package_size} ${p.unit==='piece'?'Stück':'g'}`:`${p.amount} ${p.unit==='piece'?'Stück':'g'}`).join(' + ')||'0'}
export function filterItems(items,query){const q=query.trim().toLocaleLowerCase('de');return q?items.filter(i=>(i.product+' '+formatQuantity(i.parts)+' '+(i.note||'')).toLocaleLowerCase('de').includes(q)):items}
export function nextTheme(current){return current==='system'?'light':current==='light'?'dark':'system'}
export function applyTheme(value,root=document.documentElement){if(value==='system')root.removeAttribute('data-theme');else root.dataset.theme=value;return value}
export function chooseActiveFreezer(freezers,current){return current&&freezers.some(f=>f.id===current)?current:freezers.find(f=>f.is_default)?.id??freezers[0]?.id??null}
