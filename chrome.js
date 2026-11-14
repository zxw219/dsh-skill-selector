import {access} from 'node:fs/promises';
import {spawn} from 'node:child_process';
import {join} from 'node:path';
import {originals} from './originals.js';

export async function chromeLaunchSpec(id, env=process.env, exists=async path=>{try{await access(path);return true;}catch{return false;}}) {
  const site=originals.find(item=>item.id===id&&item.kind==='web');
  if(!site)throw Error('请选择工作台中的原版网站入口');
  const roots=[env.ProgramFiles,env['ProgramFiles(x86)'],env.LOCALAPPDATA].filter(Boolean);
  for(const root of roots){
    const executable=join(root,'Google','Chrome','Application','chrome.exe');
    if(await exists(executable))return {executable,args:['--new-window',site.url],site};
  }
  throw Error('未找到 Google Chrome，请安装 Chrome 后重试。');
}

export async function openOriginalInChrome(id) {
  if(process.platform!=='win32')throw Error('当前 Chrome 启动入口适用于 Windows 桌面版。');
  const {executable,args,site}=await chromeLaunchSpec(id);
  await new Promise((resolve,reject)=>{
    const child=spawn(executable,args,{detached:true,stdio:'ignore',windowsHide:false,shell:false});
    child.once('error',reject);
    child.once('spawn',()=>{child.unref();resolve();});
  });
  return {ok:true,id:site.id,url:site.url,notice:'已向 Chrome 发出新窗口打开请求；Chrome 未运行时会自动启动。'};
}
