export function formatQuantity(parts){return parts.map(p=>p.kind==='package'?`${p.amount} × ${p.package_size} ${p.unit==='piece'?'Stück':'g'}`:`${p.amount} ${p.unit==='piece'?'Stück':'g'}`).join(' + ')||'0'}
export function filterItems(items,query){const q=query.trim().toLocaleLowerCase('de');return q?items.filter(i=>(i.product+' '+formatQuantity(i.parts)+' '+(i.note||'')).toLocaleLowerCase('de').includes(q)):items}
export function effectiveTheme(preference,systemDark){return preference==='light'||preference==='dark'?preference:systemDark?'dark':'light'}
export function nextTheme(current){return current==='dark'?'light':'dark'}
export function applyTheme(value,root=document.documentElement){if(value==='system')root.removeAttribute('data-theme');else root.dataset.theme=value;return value}
export function updateThemeButton(button,current){const next=nextTheme(current);button.textContent=next==='dark'?'☾':'☀';button.title=`Auf ${next==='dark'?'dunkles':'helles'} Farbschema wechseln`;button.setAttribute('aria-label',`${button.title}; aktuell ${current==='dark'?'dunkel':'hell'}`)}
export function chooseActiveFreezer(freezers,current){return current&&freezers.some(f=>f.id===current)?current:freezers.find(f=>f.is_default)?.id??freezers[0]?.id??null}
export function normalizeProduct(value){return value.trim().toLocaleLowerCase('de')}
export function quantityDimension(parts){const unit=parts.find(part=>Number(part.amount)>0)?.unit;return unit==='piece'?'count':unit?'weight':null}
export function findMergeCandidates(items,product,parts){const name=normalizeProduct(product);const dimension=quantityDimension(parts);return items.filter(item=>normalizeProduct(item.product)===name&&item.dimension===dimension)}
export function formatAuditValue(value){if(value===null||value===undefined)return '—';if(typeof value==='object')return JSON.stringify(value,null,2);if(value==='')return '„“';return String(value)}
export function auditChanges(before,after){const oldValue=before||{};const newValue=after||{};return [...new Set([...Object.keys(oldValue),...Object.keys(newValue)])].filter(field=>JSON.stringify(oldValue[field])!==JSON.stringify(newValue[field])).map(field=>({field,before:oldValue[field],after:newValue[field]}))}
