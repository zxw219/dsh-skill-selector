/* Native skill selector client. React is supplied by the DSH module loader. */
window.__ModuleLoader__.load({
  id: 'dsh-skill-selector-session',
  factory(require) {
    const React = require('react');
    const h = React.createElement;
    const NS = 'dsh-prompt-workbench';
    const PANEL = 'prompt-workbench';
    const STATUSES = ['testing', 'keep', 'watch', 'retired'];
    const en = {
      title: 'Skill selector', subtitle: 'Choose a skill for this conversation.',
      manualMode: 'Manual skill mode · current session', manualOn: 'On · allowlist automatic, others manual', manualOff: 'Off · native invocation rules', manualHelp: 'Applies only to this session. When on, allowlisted skills may load automatically; other skills require a selected draft or a leading /skill-name command. When off, native invocation rules apply. Previously loaded content stays in history.', manualChanged: 'Session invocation mode saved.',
      sessionAllow: 'Allow automatic loading in this session', defaultAllow: 'Allow automatic loading by default in future sessions', allowlistManage: 'Manage automatic skill allowlists', sessionAllowlist: 'Current session allowlist', defaultAllowlist: 'Default allowlist for future sessions', allowlistCount: 'Current session: {count}', defaultAllowlistCount: 'Default: {count}', allowlistEmpty: 'No skills allowed automatically.', defaultAllowlistHelp: 'Default changes apply only when a future session first resolves its policy. They never change this session. Configure default checkboxes separately.', allowlistSaved: 'Current session allowlist saved.', defaultAllowlistSaved: 'Default allowlist saved; this session is unchanged.', autoUnavailable: 'Only model-invocable native skills can be added. Pack and user-only skills require manual selection; stored entries can still be removed.', missingSkill: 'Not in the current catalog',
      allSkills: 'All skills', details: 'Details', filters: 'Filters', optionalNote: 'Add a note (optional)', more: 'More options', selectedEmpty: 'No skill selected', readyToUse: 'Ready for your task', starRating: '{count} out of 5 stars', savedReview: 'Review saved successfully.', selectionHelp: 'Choose a skill below to get started.', combinationSetup: 'Selected combination · roles and order', shortUse: 'Use · add to draft', shortCombine: 'Combination preview', shortHistory: 'History', footerSingle: 'Adds to this draft. Send when ready.', footerCombine: 'Review the preview, then add it to your draft.', backToSkills: 'Back to skill selection',

      recommend: 'Help me choose a skill', recommendations: 'Suggested skills', recommendationHelp: 'Matches task keywords and skill tags; this is not an effectiveness rating.', recommendationEmpty: 'No suggestions for this task. Browse the catalog or add more detail.', briefRequired: 'Describe your task first.',
      mode: 'Usage mode', single: 'Single skill', combination: 'Combine skills', singleHelp: 'Choose one skill for everyday use.', use: 'Use skill · add to draft', useRequired: 'Choose one available, non-retired skill and describe your task.', useHelp: 'Adds a skill invocation to your draft and saves a record for later review. Check the draft and send when ready.',
      combinationHelp: 'Choose a primary skill and one or more supporting skills, with no selection limit. Supporting skills run in the order shown. Responsibilities are optional.', primarySkill: 'Primary skill', supportingSkills: 'Supporting skills · in order', supportingSkill: 'Supporting skill {count}', responsibility: 'Responsibility (optional, up to 1,000 characters)', responsibilityPlaceholder: 'Describe what this skill should handle…', moveUp: 'Move up', moveDown: 'Move down', remove: 'Remove', combine: 'Generate combined draft preview', combinePreviewHelp: 'Saves a combined record and shows a preview. Add it to the current draft yourself, then send when ready.', combineRequired: 'Choose at least two available, non-retired skills, select a primary skill, and describe your task.', combinedSaved: 'Combined record saved. Review the preview, then add it to your draft when ready.', combinationPreview: 'Combined draft preview', combinationRecord: 'Combined skill record', combinationReview: 'Review the combination as a whole', combinationReviewHelp: 'This rating applies to the whole combination and does not count toward any member’s individual skill rating.', combinationMembers: 'Combination members and responsibilities', responsibilityEmpty: 'No responsibility specified',
      selectedSingle: '{count} / 1 selected', selectedSkills: 'Selected skills',
      'category.image': 'Images', 'category.video': 'Video', 'category.storyboard': 'Storyboards', 'category.execution': 'Generation and tools', 'category.knowledge': 'Filmmaking knowledge', 'category.reverse': 'Reference analysis', 'category.writing': 'Writing', 'category.browser': 'Browser and web', 'category.documents': 'Documents', 'category.3d': '3D and previs', 'category.coding': 'Code and development', 'category.other': 'Other skills',
      skills: 'Skills', history: 'Use and review history', originals: 'Original prompt libraries', originalsHelp: 'Search the full YouMind library in conversation. Open the other original sites when you need their browser interface.',
      chromeOpened: 'Chrome received the request to open a new window.', openOriginal: 'Open in new Chrome window', useOriginal: 'Use full prompt library', refreshLibrary: 'Update full library', libraryRefreshed: 'Full prompt library updated.', originalReady: 'Library instructions added to this conversation’s draft. Send when ready.',
      draftInserted: 'Added to this conversation’s draft.', draftFallback: 'The draft changed or is unavailable. The prompt was copied instead.',
      openDraft: 'Add to current draft', draftHelp: 'Inserts at the current selection without sending. Existing draft text is preserved.',
      connecting: 'Opening conversation…', noTarget: 'Open this workbench from a conversation.', ready: 'Connected',
      search: 'Search skills', historySearch: 'Search use records', allCategories: 'All categories', allTasks: 'All tasks', allStates: 'All workbench states', favorites: 'Favorites',
      availableOnly: 'Available only', available: 'Available', disabled: 'Disabled in DSH', unavailable: 'Unavailable',
      testing: 'Testing', keep: 'Keep', watch: 'Watch', retired: 'Retired', favorite: 'Favorite', unfavorite: 'Remove favorite',
      retiredHelp: 'Retired skills are hidden by default and cannot be selected here. This does not disable the skill globally or delete its original.',
      select: 'Select', selected: 'Selected', selectedCount: '{count} selected · unlimited', clear: 'Clear selection', status: 'Workbench status',
      task: 'What would you like to do?', taskPlaceholder: 'Describe the task, expected result and any constraints…',
      trials: 'Use records', copy: 'Copy prompt', copied: 'Copied to clipboard.', clipboardError: 'Clipboard access failed. Select and copy the prompt text below.',
      saved: 'Saved.', refresh: 'Refresh', export: 'Export state JSON', exported: 'Export ready below.',
      busy: 'Working…', loading: 'Loading…', empty: 'No matching items. Adjust your search or filters.', retry: 'Retry', error: 'Operation failed',
      originalInfo: 'Original skill information', originalTitle: 'Original title', originalDescription: 'Original description', originalWhenToUse: 'Original usage guidance',
      when: 'When to use', effects: 'Side effects', source: 'Source', provider: 'Provider', guidance: 'Curated guidance; check the skill before use.',
      reviews: 'reviews', review: 'Review use record', rating: 'Rating', note: 'Review note', notePlaceholder: 'What worked, what failed, and what would you change?', saveReview: 'Save review',
      noHistory: 'No saved records yet. Use a skill or combine skills to start.', reviewSaved: 'Review saved.', showPrompt: 'Prompt', exportedState: 'Exported workbench state', close: 'Close',
      unknownResponse: 'The Host returned an unexpected workbench response.', commandMissing: 'The /prompt-workbench command is unavailable in this conversation.',
      outcome: 'Saved reviews', noReviews: 'No reviews yet.', unchanged: 'Keep current status',
      originalsUnavailable: 'Original library entries are unavailable. Refresh to retry.', browserError: 'The original site could not be opened.',
    };
    const zh = {
      title: '技能选择器', subtitle: '为当前会话选择合适的技能。',
      manualMode: '手动技能模式 · 当前会话', manualOn: '已开启 · 白名单自动，其他手动', manualOff: '已关闭 · 使用原生调用规则', manualHelp: '仅对当前会话生效。开启时，白名单技能可自动加载，其他技能需发送选择草稿或开头独立的 /技能名。关闭时使用原生调用规则。已加载内容仍留在历史中。', manualChanged: '当前会话技能调用模式已保存。',
      sessionAllow: '允许当前会话自动加载', defaultAllow: '默认允许未来会话自动加载', allowlistManage: '管理自动技能白名单', sessionAllowlist: '当前会话白名单', defaultAllowlist: '未来会话默认白名单', allowlistCount: '当前会话：{count}', defaultAllowlistCount: '默认：{count}', allowlistEmpty: '暂未允许任何技能自动加载。', defaultAllowlistHelp: '默认更改仅在未来会话首次解析策略时生效，绝不修改当前会话。请单独设置默认复选框。', allowlistSaved: '当前会话白名单已保存。', defaultAllowlistSaved: '默认白名单已保存，当前会话不变。', autoUnavailable: '仅可添加模型可调用的原生技能。技能包与仅用户可调用的技能需手动选择；已存条目仍可移除。', missingSkill: '当前目录中不存在',
      allSkills: '全部技能', details: '详细说明', filters: '筛选', optionalNote: '添加说明（选填）', more: '更多操作', selectedEmpty: '尚未选择技能', readyToUse: '为这次任务准备', starRating: '{count} 星，满分 5 星', savedReview: '评价已保存成功。', selectionHelp: '从下方选择一个技能开始。', combinationSetup: '已选组合 · 职责与顺序', shortUse: '使用 · 加入草稿', shortCombine: '组合预览', shortHistory: '历史', footerSingle: '加入当前草稿，检查后自行发送。', footerCombine: '先检查组合预览，再加入当前草稿。', backToSkills: '返回技能选择',

      recommend: '帮我挑技能', recommendations: '建议试试', recommendationHelp: '按任务关键词与技能标签匹配，用途匹配，不是效果评分。', recommendationEmpty: '暂未找到建议，可补充任务描述或直接浏览技能。', briefRequired: '请先写下要完成的任务。',
      mode: '使用模式', single: '单独使用', combination: '组合使用', singleHelp: '日常选择 1 个技能使用。', use: '使用技能 · 加入草稿', useRequired: '请选择 1 个可用且未停用的技能，并填写任务。', useHelp: '将技能调用加入草稿，并保存记录供之后评价。检查后自行发送。',
      combinationHelp: '选择 1 个主技能和多个辅助技能，数量不限。辅助技能按下方顺序处理，各自职责可选填写。', primarySkill: '主技能', supportingSkills: '辅助技能 · 按顺序处理', supportingSkill: '辅助技能 {count}', responsibility: '职责（选填，最多 1000 字符）', responsibilityPlaceholder: '填写该技能负责处理的内容…', moveUp: '上移', moveDown: '下移', remove: '去除', combine: '生成组合草稿预览', combinePreviewHelp: '仅保存组合记录并显示预览，检查后自行点击“加入当前草稿”再发送。', combineRequired: '请选择至少 2 个可用且未停用的技能，指定主技能并填写任务。', combinedSaved: '组合记录已保存，请检查预览，自行加入当前草稿后发送。', combinationPreview: '组合草稿预览', combinationRecord: '组合使用记录', combinationReview: '组合整体评价', combinationReviewHelp: '评分针对组合整体，不计入任何成员技能的独立质量评分。', combinationMembers: '组合成员与职责', responsibilityEmpty: '未填写职责',
      selectedSingle: '已选择 {count} / 1', selectedSkills: '已选技能',
      'category.image': '图像创作', 'category.video': '视频创作', 'category.storyboard': '分镜与导演', 'category.execution': '生成与工具', 'category.knowledge': '影视知识', 'category.reverse': '参考解析', 'category.writing': '写作', 'category.browser': '浏览器与网络', 'category.documents': '文档与表格', 'category.3d': '三维与预演', 'category.coding': '代码与开发', 'category.other': '其他技能',
      skills: '技能', history: '使用与评价历史', originals: '原版提示词库', originalsHelp: '在对话中检索 YouMind 完整提示词库；需要网站界面时，点击打开其他原版网站。',
      chromeOpened: '已请求 Chrome 新窗口打开，未运行时会自动启动。', openOriginal: '在 Chrome 新窗口打开', useOriginal: '使用完整提示词库', refreshLibrary: '更新完整库', libraryRefreshed: '完整提示词库已更新。', originalReady: '提示词库使用说明已加入当前会话草稿，可检查后发送。',
      draftInserted: '已加入当前会话草稿。', draftFallback: '草稿已变化或暂不可用，已改为复制提示词。',
      openDraft: '加入当前草稿', draftHelp: '在当前光标处插入，不自动发送，并保留已有草稿。',
      connecting: '正在打开会话…', noTarget: '请从会话中打开工作台。', ready: '已连接',
      search: '搜索技能', historySearch: '搜索使用记录', allCategories: '全部分类', allTasks: '全部任务', allStates: '全部工作台状态', favorites: '收藏',
      availableOnly: '仅显示可用', available: '可用', disabled: 'DSH 中已禁用', unavailable: '不可用',
      testing: '测试中', keep: '保留', watch: '观察', retired: '隐藏', favorite: '收藏', unfavorite: '取消收藏',
      retiredHelp: '停用技能默认隐藏，不能在此选择；不会全局禁用技能或删除原文件。',
      select: '选择', selected: '已选择', selectedCount: '已选择 {count} 个 · 数量无限制', clear: '清空选择', status: '工作台状态',
      task: '这次想做什么？', taskPlaceholder: '描述任务、期望结果和限制条件…',
      trials: '使用记录', copy: '复制提示词', copied: '已复制到剪贴板。', clipboardError: '无法访问剪贴板，请选中下方提示词手动复制。',
      saved: '已保存。', refresh: '刷新', export: '导出状态 JSON', exported: '导出结果已显示在下方。',
      busy: '处理中…', loading: '加载中…', empty: '没有匹配项目，请调整搜索或筛选。', retry: '重试', error: '操作失败',
      originalInfo: '查看原版简介', originalTitle: '原版标题', originalDescription: '原版简介', originalWhenToUse: '原版适用场景',
      when: '适用场景', effects: '副作用', source: '来源', provider: '提供方', guidance: '以下为整理后的使用提示，请以技能实际说明为准。',
      reviews: '条评价', review: '评价使用记录', rating: '评分', note: '评价说明', notePlaceholder: '哪些有效，哪些失败，下次要改什么？', saveReview: '保存评价',
      noHistory: '暂无记录。单独使用或组合使用技能后，会保存在这里。', reviewSaved: '评价已保存。', showPrompt: '提示词', exportedState: '工作台状态导出', close: '关闭',
      unknownResponse: '主机返回了无法识别的工作台响应。', commandMissing: '该会话中尚未提供 /prompt-workbench 命令。',
      outcome: '已保存评价', noReviews: '暂无评价。', unchanged: '保留当前状态',
      originalsUnavailable: '暂时无法读取原版提示词库入口，请刷新重试。', browserError: '无法在 Chrome 新窗口打开。',
    };
    const CSS = `
.pw-root{height:100%;min-height:0;min-width:0;display:flex;flex-direction:column;overflow:hidden;background:var(--dsw-alias-bg-base);color:var(--dsw-alias-label-primary);font:inherit;font-size:13px;line-height:1.55;container-type:inline-size}.pw-root *{box-sizing:border-box}.pw-body{flex:1;min-height:0;min-width:0;overflow:auto;overscroll-behavior:contain;padding:16px 14px 20px;scroll-padding-block:12px}.pw-header{display:flex;align-items:flex-start;justify-content:space-between;gap:8px;margin-bottom:18px}.pw-heading{margin:0;font-size:17px;line-height:1.4;font-weight:600}.pw-subtitle,.pw-muted{color:var(--dsw-alias-label-secondary);overflow-wrap:anywhere}.pw-subtitle{margin:4px 0 0;font-size:12px}.pw-row{display:flex;align-items:center;gap:8px;flex-wrap:wrap}.pw-between{justify-content:space-between}.pw-field{display:flex;flex-direction:column;gap:6px;min-width:0}.pw-label{font-size:12px;color:var(--dsw-alias-label-secondary)}.pw-input,.pw-select,.pw-textarea,.pw-prompt{font:inherit;width:100%;min-width:0;border:1px solid var(--dsw-alias-border-l1);border-radius:8px;background:var(--dsw-alias-bg-layer-1);color:var(--dsw-alias-label-primary);padding:8px 10px;min-height:36px}.pw-textarea{resize:vertical;min-height:82px;line-height:1.55}.pw-prompt{resize:vertical;min-height:150px;font-family:monospace;font-size:12px}.pw-root :is(button,input,select,textarea,summary):focus-visible,.pw-header-entry:focus-visible{outline:2px solid var(--dsw-alias-brand-primary);outline-offset:2px}.pw-button{font:inherit;cursor:pointer;display:inline-flex;justify-content:center;align-items:center;gap:6px;min-height:34px;padding:6px 10px;border:1px solid var(--dsw-alias-border-l1);border-radius:7px;background:var(--dsw-alias-bg-layer-1);color:var(--dsw-alias-label-primary);white-space:normal;text-align:center;transition:background-color 140ms ease,border-color 140ms ease,opacity 140ms ease}.pw-button:not(:disabled):hover,.pw-tab:hover{background:var(--dsw-alias-bg-layer-1)}.pw-button:disabled{opacity:.45;cursor:not-allowed}.pw-primary,.pw-primary:not(:disabled):hover{background:var(--dsw-alias-brand-primary);color:var(--dsw-alias-label-primary-inverted);border-color:var(--dsw-alias-brand-primary)}.pw-quiet{background:transparent;border-color:transparent}.pw-help{font-size:12px;color:var(--dsw-alias-label-secondary);margin:8px 0;overflow-wrap:anywhere}.pw-tabs{display:flex;gap:4px;border-bottom:1px solid var(--dsw-alias-border-l1);margin-bottom:16px}.pw-tab{font:inherit;flex:1;min-width:0;min-height:38px;padding:8px 4px;border:0;border-bottom:2px solid transparent;background:transparent;color:var(--dsw-alias-label-secondary);cursor:pointer;transition:color 140ms ease,border-color 140ms ease}.pw-tab:disabled{opacity:.55;cursor:wait}.pw-tab[aria-selected=true]{color:var(--dsw-alias-label-primary);border-bottom-color:var(--dsw-alias-brand-primary);font-weight:600}.pw-builder{display:flex;flex-direction:column;gap:10px;margin-bottom:16px}.pw-segmented{display:flex;gap:3px;padding:3px;border:1px solid var(--dsw-alias-border-l1);border-radius:9px;background:var(--dsw-alias-bg-layer-1)}.pw-segmented .pw-button{flex:1;min-width:0;background:transparent;border-color:transparent}.pw-segmented .pw-button[aria-pressed=true]{background:var(--dsw-alias-bg-base);border-color:var(--dsw-alias-border-l1);font-weight:600}.pw-filters{display:grid;grid-template-columns:1fr;gap:8px;margin:10px 0}.pw-filter-grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:8px;margin-top:10px}.pw-check{display:flex;align-items:center;gap:6px;font-size:12px;color:var(--dsw-alias-label-secondary)}.pw-check input{accent-color:var(--dsw-alias-brand-primary)}.pw-grid{display:grid;grid-template-columns:minmax(0,1fr);gap:8px;margin-top:12px}.pw-card{min-width:0;padding:12px;border:1px solid var(--dsw-alias-border-l1);border-radius:10px;background:var(--dsw-alias-bg-layer-1);transition:border-color 150ms ease,background-color 150ms ease}.pw-card.pw-picked{border-color:var(--dsw-alias-brand-primary)}.pw-card-top{display:flex;align-items:flex-start;justify-content:space-between;gap:8px}.pw-card-title{margin:0;font-size:13px;line-height:1.5;font-weight:600;overflow-wrap:anywhere}.pw-card-top>.pw-card-title{padding-top:4px}.pw-card p{margin:8px 0;overflow-wrap:anywhere}.pw-purpose{overflow:hidden;white-space:nowrap;text-overflow:ellipsis;color:var(--dsw-alias-label-secondary)}.pw-rating-summary{font-size:12px;color:var(--dsw-alias-label-secondary)}.pw-card-foot{display:flex;align-items:center;justify-content:space-between;gap:8px;flex-wrap:wrap;margin-top:10px}.pw-card-foot>.pw-select{width:auto;max-width:100%}.pw-badges{display:flex;gap:5px;flex-wrap:wrap}.pw-badge{display:inline-flex;align-items:center;padding:2px 6px;border:1px solid var(--dsw-alias-border-l1);border-radius:5px;font-size:11px;color:var(--dsw-alias-label-secondary);overflow-wrap:anywhere}.pw-available{color:var(--dsw-alias-label-primary)}.pw-root details{min-width:0}.pw-root summary{cursor:pointer;color:var(--dsw-alias-label-secondary);font-size:12px;min-height:30px;padding:5px 0;overflow-wrap:anywhere}.pw-root details[open]>summary{color:var(--dsw-alias-label-primary)}.pw-details{margin-top:8px;border-top:1px solid var(--dsw-alias-border-l1);padding-top:3px}.pw-details .pw-field{margin:10px 0}.pw-detail-id{font-family:monospace;font-size:11px;overflow-wrap:anywhere}.pw-section-title{font-size:13px;font-weight:600;margin:0 0 8px}.pw-review{border-top:1px solid var(--dsw-alias-border-l1);margin-top:12px;padding-top:12px;display:flex;flex-direction:column;gap:10px}.pw-review-grid{display:grid;grid-template-columns:minmax(0,1fr);gap:10px}.pw-review-note{min-height:70px}.pw-stars{display:flex;gap:3px;flex-wrap:wrap}.pw-star{font-size:21px;line-height:1;min-width:34px;padding:6px}.pw-star[aria-pressed=true]{border-color:var(--dsw-alias-brand-primary);color:var(--dsw-alias-brand-primary)}.pw-saved-review{padding:10px;border:1px solid var(--dsw-alias-border-l1);border-radius:8px;margin-top:8px;overflow-wrap:anywhere}.pw-saved-review .pw-field{margin-top:8px}.pw-trial{margin:12px 0}.pw-trial>.pw-row{margin-top:8px}.pw-notice{border:1px solid var(--dsw-alias-border-l1);border-radius:8px;padding:10px;margin:0 0 12px;background:var(--dsw-alias-bg-layer-1);overflow-wrap:anywhere}.pw-review-success{font-size:12px;color:var(--dsw-alias-label-primary);margin:0}.pw-empty{padding:24px 10px;text-align:center;color:var(--dsw-alias-label-secondary)}.pw-originals{border-top:1px solid var(--dsw-alias-border-l1);margin-top:20px;padding-top:12px}.pw-originals>summary{font-weight:600;font-size:13px}.pw-toolbar{margin-top:12px;border-top:1px solid var(--dsw-alias-border-l1);padding-top:8px}.pw-actionbar{flex:none;min-width:0;max-height:45%;overflow:auto;position:sticky;bottom:0;padding:10px 14px 12px;background:var(--dsw-alias-bg-base);border-top:1px solid var(--dsw-alias-border-l1);display:flex;flex-direction:column;gap:8px}.pw-selection-summary{flex:1;min-width:0;display:flex;flex-direction:column;gap:2px}.pw-selection-summary strong{font-size:12px;font-weight:600;overflow:hidden;white-space:nowrap;text-overflow:ellipsis}.pw-selection-summary .pw-muted{font-size:11px}.pw-actionbar .pw-help{margin:0}.pw-actions{display:flex;gap:6px;flex-wrap:wrap}.pw-actions>.pw-button{flex:1;min-width:0}.pw-header-entry{display:inline-flex;align-items:center;justify-content:center;width:28px;height:28px;padding:4px;border:0;border-radius:6px;background:transparent;color:var(--dsw-alias-label-secondary);cursor:pointer}.pw-header-entry:hover{background:var(--dsw-alias-bg-layer-1);color:var(--dsw-alias-label-primary)}
/* Theme-derived accents distinguish selection, roles and feedback in both themes. */
.pw-root{--pw-blue:var(--dsw-alias-brand-primary);--pw-purple:color-mix(in oklch,var(--dsw-alias-brand-primary) 65%,var(--dsw-alias-state-error-primary));--pw-gold:var(--dsw-alias-state-warn-primary);--pw-green:var(--dsw-alias-state-success-primary);--pw-red:var(--dsw-alias-state-error-primary);--pw-edge:color-mix(in srgb,var(--pw-blue) 22%,var(--dsw-alias-border-l1));--pw-soft-blue:color-mix(in srgb,var(--pw-blue) 7%,var(--dsw-alias-bg-layer-1))}
.pw-card{border-color:var(--pw-edge)}
.pw-card:hover{border-color:color-mix(in srgb,var(--pw-blue) 50%,var(--dsw-alias-border-l2))}
.pw-card.pw-picked{border-color:var(--pw-blue);background:var(--pw-soft-blue)}
.pw-card.pw-picked.pw-role-primary{border-color:var(--pw-purple);background:color-mix(in srgb,var(--pw-purple) 8%,var(--dsw-alias-bg-layer-1))}
.pw-card .pw-select-button[aria-pressed=true]{border-color:var(--pw-blue);color:var(--dsw-alias-label-primary);background:color-mix(in srgb,var(--pw-blue) 12%,var(--dsw-alias-bg-layer-1))}
.pw-card.pw-role-primary .pw-select-button[aria-pressed=true]{border-color:var(--pw-purple);background:color-mix(in srgb,var(--pw-purple) 12%,var(--dsw-alias-bg-layer-1))}
.pw-favorite[aria-pressed=true],.pw-favorite[aria-pressed=true]:not(:disabled):hover{color:var(--pw-gold);border-color:color-mix(in srgb,var(--pw-gold) 45%,var(--dsw-alias-border-l1));background:color-mix(in srgb,var(--pw-gold) 9%,var(--dsw-alias-bg-layer-1))}
.pw-input,.pw-select,.pw-textarea,.pw-prompt,.pw-segmented{border-color:var(--pw-edge)}
.pw-tab[aria-selected=true]{border-bottom-color:var(--pw-blue);background:var(--pw-soft-blue)}
.pw-segmented .pw-button[aria-pressed=true]{border-color:var(--pw-blue);background:var(--pw-soft-blue)}
.pw-role-primary.pw-saved-review{border-color:var(--pw-purple);background:color-mix(in srgb,var(--pw-purple) 6%,var(--dsw-alias-bg-base))}
.pw-role-support.pw-saved-review{border-color:color-mix(in srgb,var(--pw-blue) 42%,var(--dsw-alias-border-l1));background:color-mix(in srgb,var(--pw-blue) 4%,var(--dsw-alias-bg-base))}
.pw-role-primary .pw-badge{border-color:var(--pw-purple)}
.pw-role-support .pw-badge{border-color:var(--pw-blue)}
.pw-star.pw-star-filled{color:var(--pw-gold)}
.pw-star[aria-pressed=true]{color:var(--pw-gold);border-color:var(--pw-gold);background:color-mix(in srgb,var(--pw-gold) 8%,var(--dsw-alias-bg-layer-1))}
.pw-notice-success{border-color:var(--pw-green);background:color-mix(in srgb,var(--pw-green) 7%,var(--dsw-alias-bg-layer-1))}
.pw-notice-error{border-color:var(--pw-red);background:color-mix(in srgb,var(--pw-red) 7%,var(--dsw-alias-bg-layer-1))}
.pw-review-success{color:var(--pw-green)}
.pw-actionbar{border-top-color:color-mix(in srgb,var(--pw-blue) 45%,var(--dsw-alias-border-l1));background:color-mix(in srgb,var(--pw-blue) 3%,var(--dsw-alias-bg-base))}
@container(max-width:300px){.pw-body{padding:12px 10px 16px}.pw-filter-grid{grid-template-columns:minmax(0,1fr)}.pw-actionbar{padding:10px}.pw-actions{flex-direction:column}.pw-card{padding:10px}.pw-card-foot{align-items:stretch}.pw-card-foot>.pw-select{width:100%}}
@media(prefers-reduced-motion:reduce){.pw-root *{transition:none!important;scroll-behavior:auto!important}}
`;
    function text(value) {
      if (value == null) return '';
      if (typeof value === 'string') return value;
      if (Array.isArray(value)) return value.map(text).filter(Boolean).join(' · ');
      return typeof value === 'object' ? String(value.label || value.title || value.name || value.id || JSON.stringify(value)) : String(value);
    }
    function Icon({ size = 18 }) {
      return h('svg', { viewBox: '0 0 24 24', width: size, height: size, fill: 'none', stroke: 'currentColor', strokeWidth: 1.6, strokeLinecap: 'round', strokeLinejoin: 'round', 'aria-hidden': true },
        h('path', { d: 'M5 4.5h9a2 2 0 0 1 2 2V10M5 4.5a2 2 0 0 0-2 2v13h11M5 4.5v15M8 8h5M8 11h3' }),
        h('path', { d: 'm17.5 11 .9 3.1 3.1.9-3.1.9-.9 3.1-.9-3.1-3.1-.9 3.1-.9.9-3.1ZM10 16h1M19 4v4M17 6h4' }));
    }
    function Field({ label, children }) { return h('label', { className: 'pw-field' }, h('span', { className: 'pw-label' }, label), children); }
    function Button({ children, primary, quiet, className = '', ...props }) { return h('button', { type: 'button', ...props, className: 'pw-button' + (primary ? ' pw-primary' : '') + (quiet ? ' pw-quiet' : '') + (className ? ' ' + className : '') }, children); }
    function Select({ label, value, onChange, options, disabled }) { return h('select', { className: 'pw-select', 'aria-label': label, value, disabled, onChange: e => onChange(e.target.value) }, options.map(option => h('option', { key: option.value, value: option.value }, option.label))); }
    function PromptResult({ title, prompt, t, onCopy, onDraft, children }) {
      return h('article', { className: 'pw-card pw-trial' }, h('h3', { className: 'pw-card-title' }, title),
        h('textarea', { className: 'pw-prompt', readOnly: true, value: prompt || '', 'aria-label': t('showPrompt') }),
        h('div', { className: 'pw-row' }, h(Button, { onClick: () => void onCopy(prompt) }, t('copy')), h(Button, { onClick: () => void onDraft(prompt) }, t('openDraft'))),
        h('p', { className: 'pw-help' }, t('draftHelp')), children);
    }
    function ReviewForm({ trial, t, disabled, onSave }) {
      const [rating, setRating] = React.useState(5);
      const [note, setNote] = React.useState('');
      const [status, setStatus] = React.useState('');
      const [saved, setSaved] = React.useState(false);
      const combination = trial.kind === 'combination';
      function changeRating(value) { setRating(value); setSaved(false); }
      return h('form', { className: 'pw-review', onSubmit: async e => {
        e.preventDefault();
        const success = await onSave({ skillId: trial.skillId, trialId: trial.id, rating, note, ...(!combination && status ? { status } : {}) });
        if (success) setSaved(true);
      } },
        h('h4', { className: 'pw-card-title' }, t(combination ? 'combinationReview' : 'review')),
        combination && h('p', { className: 'pw-help' }, t('combinationReviewHelp')),
        h('div', { className: 'pw-review-grid' },
          h('div', { className: 'pw-field' }, h('span', { className: 'pw-label' }, t('rating') + ' · ' + rating + '/5'),
            h('div', { className: 'pw-stars', role: 'group', 'aria-label': t('rating') }, [1, 2, 3, 4, 5].map(n => h(Button, {
              key: n, disabled, 'aria-label': t('starRating', { count: n }), 'aria-pressed': rating === n,
              tabIndex: rating === n ? 0 : -1, onClick: () => changeRating(n),
              onKeyDown: e => {
                if (!['ArrowLeft', 'ArrowRight', 'ArrowUp', 'ArrowDown', 'Home', 'End'].includes(e.key)) return;
                e.preventDefault();
                const next = e.key === 'Home' ? 1 : e.key === 'End' ? 5 : Math.max(1, Math.min(5, n + (e.key === 'ArrowLeft' || e.key === 'ArrowDown' ? -1 : 1)));
                changeRating(next); e.currentTarget.parentNode.children[next - 1].focus();
              }, className: 'pw-star' + (n <= rating ? ' pw-star-filled' : ''),
            }, h('span', { 'aria-hidden': true }, n <= rating ? '★' : '☆'))))),
          !combination && h(Field, { label: t('status') }, h(Select, { label: t('status'), value: status, onChange: value => { setStatus(value); setSaved(false); }, disabled, options: [{ value: '', label: t('unchanged') }, ...STATUSES.map(value => ({ value, label: t(value) }))] }))),
        h('details', null, h('summary', null, t('optionalNote')), h(Field, { label: t('note') }, h('textarea', { className: 'pw-textarea pw-review-note', value: note, onChange: e => { setNote(e.target.value); setSaved(false); }, placeholder: t('notePlaceholder'), disabled }))),
        h('div', { className: 'pw-card-foot' }, h(Button, { type: 'submit', disabled, primary: true }, t('saveReview')), saved && h('p', { className: 'pw-review-success', role: 'status' }, '✓ ' + t('savedReview'))));
    }
    // Each body is keyed by its native Session identity. No manual target selector or new-session draft routing.
    function Panel({ ctx, t, sessionId: target, inputActions }) {
      const [connection, setConnection] = React.useState('idle');
      const [connectAttempt, setConnectAttempt] = React.useState(0);
      const [tab, setTab] = React.useState('skills');
      const [query, setQuery] = React.useState('');
      const [category, setCategory] = React.useState('');
      const [taskFilter, setTaskFilter] = React.useState('');
      const [statusFilter, setStatusFilter] = React.useState('');
      const [availableOnly, setAvailableOnly] = React.useState(true);
      const [mode, setMode] = React.useState('single');
      const combination = mode === 'combination';
      const [primaryId, setPrimaryId] = React.useState('');
      const [roles, setRoles] = React.useState({});
      const [recommendations, setRecommendations] = React.useState(null);
      const [catalog, setCatalog] = React.useState({ skills: [], stats: {} });
      const [originals, setOriginals] = React.useState([]);
      const [manualMode, setManualMode] = React.useState(null);
      const [selected, setSelected] = React.useState([]);
      const [brief, setBrief] = React.useState('');
      const [usageRecords, setUsageRecords] = React.useState([]);
      const [history, setHistory] = React.useState({ trials: [], reviews: [] });
      const [exported, setExported] = React.useState('');
      const [busy, setBusy] = React.useState('');
      const [loading, setLoading] = React.useState(false);
      const [notice, setNotice] = React.useState(null);
      const retained = React.useRef(null);
      const generation = React.useRef(0);
      const requestSequence = React.useRef(0);
      const activeOperation = React.useRef(false);
      const mounted = React.useRef(true);
      React.useEffect(() => {
        setPrimaryId(current => selected.includes(current) ? current : selected[0] || '');
        setRoles(current => Object.fromEntries(selected.filter(id => Object.prototype.hasOwnProperty.call(current, id)).map(id => [id, current[id]])));
        setUsageRecords([]);
      }, [selected]);
      React.useEffect(() => { mounted.current = true; return () => { mounted.current = false; generation.current++; requestSequence.current++; }; }, []);
      React.useEffect(() => {
        const current = ++generation.current;
        requestSequence.current++;
        activeOperation.current = false;
        if (!target) { setConnection('idle'); return undefined; }
        let reference;
        setConnection('loading');
        try {
          reference = ctx.sessions.retain(target, { source: 'controllerOperation' });
          retained.current = reference;
          reference.ready.then(() => { if (mounted.current && generation.current === current) setConnection('ready'); }, error => {
            if (mounted.current && generation.current === current) { setConnection('error'); setNotice({ error: true, text: error.message || String(error) }); }
          });
        } catch (error) { setConnection('error'); setNotice({ error: true, text: error.message || String(error) }); }
        return () => { generation.current++; if (retained.current === reference) retained.current = null; if (reference) reference.release(); };
      }, [ctx, target, connectAttempt]);
      const call = React.useCallback(async request => {
        const reference = retained.current;
        if (!target || !reference) throw new Error(t('noTarget'));
        await reference.ready;
        const response = await ctx.remote.commands.execute(target, '/prompt-workbench ' + JSON.stringify(request), []);
        if (!response || !response.ok) throw new Error(response?.error ? response.error.message || text(response.error) : t('unknownResponse'));
        const result = response.value?.result;
        if (!result) throw new Error(t('commandMissing'));
        let payload;
        try { payload = JSON.parse(result.text || '{}'); } catch (_) { throw new Error(result.text || t('unknownResponse')); }
        if (result.kind !== 'success' || payload.ok === false || payload.error) throw new Error(text(payload.error && (payload.error.message || payload.error)) || payload.message || result.text || t('error'));
        return payload;
      }, [ctx, target, t]);
      function policyStatus(payload) {
        const status = payload?.manualMode || payload;
        if (!status || typeof status.enabled !== 'boolean' || status.scope !== 'session' || status.sessionId !== target || !Array.isArray(status.allowlist) || !Array.isArray(status.defaultAllowlist)) throw new Error(t('unknownResponse'));
        return { ...status, allowlist: [...new Set(status.allowlist.filter(id => typeof id === 'string'))], defaultAllowlist: [...new Set(status.defaultAllowlist.filter(id => typeof id === 'string'))] };
      }
      const refresh = React.useCallback(async () => {
        if (connection !== 'ready') return;
        const sequence = ++requestSequence.current;
        const current = generation.current;
        setLoading(true);
        try {
          const payload = await call({ action: tab === 'history' ? 'history' : 'list' });
          if (!mounted.current || current !== generation.current || sequence !== requestSequence.current) return;
          if (tab !== 'history') {
            const skills = payload.skills || [];
            setCatalog({ ...payload, skills });
            setSelected(ids => {
              const next = ids.filter(id => skills.some(skill => skill.id === id && skill.available && skill.status !== 'retired'));
              return next.length === ids.length ? ids : next;
            });
            if (Array.isArray(payload.originals)) setOriginals(payload.originals);
            else {
              const libraries = await call({ action: 'originals' });
              if (mounted.current && current === generation.current && sequence === requestSequence.current) setOriginals(libraries.items || []);
            }
          } else setHistory({ trials: payload.trials || [], reviews: payload.reviews || [] });
          const policy = payload.manualMode ? payload : await call({ action: 'manualMode' });
          if (mounted.current && current === generation.current && sequence === requestSequence.current) setManualMode(policyStatus(policy));
        } catch (error) { if (mounted.current && current === generation.current && sequence === requestSequence.current) setNotice({ error: true, text: error.message || String(error) }); }
        finally { if (mounted.current && current === generation.current && sequence === requestSequence.current) setLoading(false); }
      }, [call, connection, tab]);
      React.useEffect(() => { void refresh(); }, [refresh]);
      async function operate(name, request, onResult, success) {
        if (activeOperation.current) return;
        const current = generation.current;
        activeOperation.current = true;
        setBusy(name); setNotice(null);
        try {
          const payload = await call(request);
          if (!mounted.current || generation.current !== current) return;
          // Discard list/history snapshots started before this operation completed.
          // Result callbacks may start a fresh request with the new sequence.
          requestSequence.current++;
          setLoading(false);
          const message = onResult ? await onResult(payload) : undefined;
          if (mounted.current && generation.current === current) { setNotice({ error: false, text: message || success || t('saved') }); return true; }
        } catch (error) { if (mounted.current && generation.current === current) setNotice({ error: true, text: error.message || String(error) }); return false; }
        finally { if (mounted.current && generation.current === current) { activeOperation.current = false; setBusy(''); } }
      }
      function updatePolicy(action, values, success) {
        if (loading || !manualMode) return;
        void operate(action, { action, ...values }, payload => {
          setManualMode(policyStatus(payload));
          setUsageRecords([]);
        }, t(success));
      }
      function changeAllowlist(id, checked, defaults = false) {
        if (!manualMode) return;
        const ids = manualMode[defaults ? 'defaultAllowlist' : 'allowlist'];
        const next = checked ? [...new Set([...ids, id])] : ids.filter(value => value !== id);
        updatePolicy(defaults ? 'setDefaultAllowlist' : 'setAllowlist', { ids: next }, defaults ? 'defaultAllowlistSaved' : 'allowlistSaved');
      }
      async function copy(prompt) {
        try { await navigator.clipboard.writeText(prompt || ''); if (mounted.current) setNotice({ error: false, text: t('copied') }); return true; }
        catch (_) { if (mounted.current) setNotice({ error: true, text: t('clipboardError') }); return false; }
      }
      function captureDraft() {
        try { return inputActions ? { actions: inputActions, span: inputActions.captureInsertion() } : null; } catch (_) { return null; }
      }
      async function insertDraft(prompt, captured = captureDraft()) {
        if (captured && captured.actions.insertText(prompt, captured.span)) {
          captured.actions.persistDraft();
          return t('draftInserted');
        }
        if (await copy(prompt)) return t('draftFallback');
        throw new Error(t('clipboardError'));
      }
      async function openDraft(prompt) {
        try { const message = await insertDraft(prompt); if (mounted.current) setNotice({ error: false, text: message }); }
        catch (error) { if (mounted.current) setNotice({ error: true, text: error.message || String(error) }); }
      }
      function activateOriginal(item) {
        if (item.kind === 'web') {
          void operate('openWebsite', { action: 'openWebsite', id: item.id }, undefined, t('chromeOpened'));
          return;
        }
        const captured = captureDraft();
        void operate('activate', { action: 'activate', id: item.id, brief: brief.trim() }, async payload => {
          if (typeof payload.prompt !== 'string' || !payload.prompt.trim()) throw new Error(t('unknownResponse'));
          const message = await insertDraft(payload.prompt, captured);
          return message === t('draftInserted') ? t('originalReady') : message;
        });
      }
      function setSkillStatus(skill, status, favorite) {
        if (loading) return;
        const request = { action: 'setStatus', skillId: skill.id, status };
        if (favorite !== undefined) request.favorite = favorite;
        void operate('status', request, () => {
          setCatalog(old => ({ ...old, skills: old.skills.map(row => row.id === skill.id ? { ...row, status, ...(favorite !== undefined ? { favorite } : {}) } : row) }));
          if (status === 'retired') setSelected(ids => ids.filter(id => id !== skill.id));
        });
      }
      function changeMode(value) {
        setMode(value);
        setUsageRecords([]);
        setNotice(null);
        if (value === 'single') setSelected(ids => ids.slice(0, 1));
      }
      function chooseSkill(id) {
        setUsageRecords([]);
        setSelected(ids => ids.includes(id) ? ids.filter(value => value !== id) : mode === 'single' ? [id] : [...ids, id]);
      }
      function moveSupportingSkill(id, direction) {
        setUsageRecords([]);
        setSelected(ids => {
          const supporting = ids.filter(value => value !== primaryId);
          const index = supporting.indexOf(id);
          const next = index + direction;
          if (index < 0 || next < 0 || next >= supporting.length) return ids;
          const first = ids.indexOf(id);
          const second = ids.indexOf(supporting[next]);
          const reordered = [...ids];
          [reordered[first], reordered[second]] = [reordered[second], reordered[first]];
          return reordered;
        });
      }
      function combineSkills() {
        if (selected.length < 2 || !selected.includes(primaryId) || !brief.trim()) { setNotice({ error: true, text: t('combineRequired') }); return; }
        const selectedRoles = Object.fromEntries(selected.map(id => [id, (roles[id] || '').trim().slice(0, 1000)]));
        void operate('combine', { action: 'combine', ids: selected, primaryId, roles: selectedRoles, brief: brief.trim() }, payload => {
          if (!payload.trial || payload.trial.kind !== 'combination' || typeof payload.prompt !== 'string' || !payload.prompt.trim()) throw new Error(t('unknownResponse'));
          setUsageRecords([{ ...payload.trial, prompt: payload.prompt }]);
          return [t('combinedSaved'), text(payload.notice)].filter(Boolean).join(' ');
        });
      }
      function recommendSkills() {
        if (!brief.trim()) { setNotice({ error: true, text: t('briefRequired') }); return; }
        void operate('recommend', { action: 'recommend', brief: brief.trim() }, payload => {
          if (!Array.isArray(payload.skills)) throw new Error(t('unknownResponse'));
          setRecommendations({ skills: payload.skills, notice: text(payload.notice) });
          return text(payload.notice) || t('recommendationHelp');
        });
      }
      function useSkill(e) {
        e.preventDefault();
        if (mode !== 'single') return;
        if (selected.length !== 1 || !brief.trim()) { setNotice({ error: true, text: t('useRequired') }); return; }
        // Capture the exact conversation draft before the Host request can change focus or finish later.
        const captured = captureDraft();
        void operate('use', { action: 'use', skillId: selected[0], brief: brief.trim() }, async payload => {
          if (!payload.trial || typeof payload.prompt !== 'string' || !payload.prompt.trim()) throw new Error(t('unknownResponse'));
          setUsageRecords([{ ...payload.trial, prompt: payload.prompt }]);
          const message = await insertDraft(payload.prompt, captured);
          return [message, text(payload.notice)].filter(Boolean).join(' ');
        });
      }
      const disabled = !!busy || connection !== 'ready';
      const categoryLabel = value => Object.prototype.hasOwnProperty.call(zh, 'category.' + value) ? t('category.' + value) : value;
      const options = (values, first, label = value => value) => [{ value: '', label: t(first) }, ...values.map(value => ({ value, label: label(value) }))];
      const categories = [...new Set(catalog.skills.map(skill => skill.category).filter(Boolean))];
      const tasks = [...new Set(catalog.skills.flatMap(skill => skill.tasks || skill.taskTypes || skill.platforms || []).map(text).filter(Boolean))];
      const search = query.trim().toLowerCase();
      const visibleSkills = catalog.skills.filter(skill => (tab !== 'favorites' || skill.favorite) && (!search || [skill.title, skill.description, skill.whenToUse, skill.category, skill.id, skill.platforms, skill.keywords, skill.originalTitle, skill.originalDescription, skill.originalWhenToUse].map(text).join(' ').toLowerCase().includes(search)) && (!category || skill.category === category) && (!taskFilter || (skill.tasks || skill.taskTypes || skill.platforms || []).map(text).includes(taskFilter)) && (!availableOnly || skill.available) && (statusFilter === 'retired' || skill.status !== 'retired') && (!statusFilter || (statusFilter === 'favorites' ? skill.favorite : skill.status === statusFilter)));
      const filteredTrials = history.trials.filter(trial => !search || [trial.skillTitle, trial.brief, trial.prompt, trial.model, ...(trial.members || []).flatMap(member => [member.skillId, member.title, member.role])].map(text).join(' ').toLowerCase().includes(search));
      function saveReview(request) { return operate('feedback', { action: 'feedback', ...request }, () => { void refresh(); }, t('reviewSaved')); }
      function renderTrial(trial, withReviews) {
        const reviews = withReviews ? history.reviews.filter(review => review.trialId === trial.id) : [];
        const combined = trial.kind === 'combination';
        const title = combined ? t(withReviews ? 'combinationRecord' : 'combinationPreview') : trial.skillTitle || trial.title || trial.skillId;
        return h(PromptResult, { key: trial.id, title, prompt: trial.prompt, t, onCopy: copy, onDraft: openDraft },
          h('div', { className: 'pw-muted' }, [trial.model, (trial.createdAt || trial.time) ? new Date(trial.createdAt || trial.time).toLocaleString() : ''].filter(Boolean).join(' · ')),
          combined && h('section', { className: 'pw-review', 'aria-label': t('combinationMembers') }, h('h4', { className: 'pw-card-title' }, t('combinationMembers')), (trial.members || []).map((member, index) => h('div', { className: 'pw-saved-review ' + (member.isPrimary || member.skillId === trial.primaryId ? 'pw-role-primary' : 'pw-role-support'), key: member.skillId || index },
            h('div', { className: 'pw-row' }, h('span', { className: 'pw-badge' }, member.isPrimary || member.skillId === trial.primaryId ? t('primarySkill') : t('supportingSkill', { count: index })), h('strong', null, member.title || member.skillId)),
            h('p', { style: { whiteSpace: 'pre-wrap', overflowWrap: 'anywhere' } }, member.role || t('responsibilityEmpty'))))),
          h(ReviewForm, { trial, t, disabled, onSave: saveReview }),
          withReviews && h('div', { className: 'pw-review' }, h('h4', { className: 'pw-card-title' }, t(combined ? 'combinationReview' : 'outcome')),
            reviews.length ? reviews.map((review, index) => h('div', { key: review.id || index, className: 'pw-saved-review' }, h('strong', null, '★'.repeat(Math.max(1, Math.min(5, Number(review.rating) || 1))) + ' ' + review.rating + '/5'), !combined && review.status && h('span', { className: 'pw-badge' }, t(review.status)), h('p', null, review.note || '—'))) : h('p', { className: 'pw-muted' }, t('noReviews'))));
      }
      function renderResponsibility(id, title) {
        return h('div', { className: 'pw-saved-review ' + (id === primaryId ? 'pw-role-primary' : 'pw-role-support'), key: id }, h('h3', { className: 'pw-card-title' }, title),
          h('div', { className: 'pw-muted' }, catalog.skills.find(skill => skill.id === id)?.title || id),
          h(Field, { label: t('responsibility') }, h('textarea', { className: 'pw-textarea pw-review-note', maxLength: 1000, value: roles[id] || '', placeholder: t('responsibilityPlaceholder'), disabled: !!busy, onChange: e => { const value = e.target.value.slice(0, 1000); setRoles(current => ({ ...current, [id]: value })); setUsageRecords([]); } })),
          h('div', { className: 'pw-muted' }, (roles[id] || '').length + '/1000'));
      }
      const tabs = ['skills', 'favorites', 'history'];
      const selectedTitles = selected.map(id => catalog.skills.find(skill => skill.id === id)?.title || id);
      function renderAllowlist(defaults = false) {
        const ids = manualMode?.[defaults ? 'defaultAllowlist' : 'allowlist'] || [];
        const label = t(defaults ? 'defaultAllowlist' : 'sessionAllowlist');
        return h('section', { 'aria-label': label }, h('h3', { className: 'pw-card-title' }, label + ' · ' + ids.length),
          ids.length ? ids.map(id => {
            const skill = catalog.skills.find(row => row.id === id);
            const title = skill?.title || id;
            return h('div', { className: 'pw-saved-review', key: id }, h('div', { className: 'pw-row pw-between' },
              h('strong', null, title), h(Button, { disabled: disabled || loading, 'aria-label': t('remove') + ': ' + title + ' · ' + label, onClick: () => changeAllowlist(id, false, defaults) }, t('remove'))),
              h('div', { className: 'pw-detail-id pw-muted' }, id), !skill && h('p', { className: 'pw-help' }, t('missingSkill')));
          }) : h('p', { className: 'pw-muted' }, t('allowlistEmpty')));
      }
      function renderSkill(skill, reason) {
        const picked = selected.includes(skill.id);
        const originalFields = ['originalTitle', 'originalDescription', 'originalWhenToUse'].filter(key => text(skill[key]).trim());
        const title = skill.title || skill.id;
        const sessionAllowed = !!manualMode?.allowlist.includes(skill.id);
        const defaultAllowed = !!manualMode?.defaultAllowlist.includes(skill.id);
        const autoEligible = skill.modelInvocable === true && skill.origin === 'existing';
        const policyDisabled = disabled || loading || !manualMode;
        return h('article', { key: skill.id, className: 'pw-card' + (picked ? ' pw-picked' + (combination && skill.id === primaryId ? ' pw-role-primary' : ' pw-role-support') : '') },
          h('div', { className: 'pw-card-top' }, h('h3', { className: 'pw-card-title' }, title), h(Button, { quiet: true, className: 'pw-favorite', disabled: disabled || loading, onClick: () => setSkillStatus(skill, skill.status || 'testing', !skill.favorite), 'aria-label': t(skill.favorite ? 'unfavorite' : 'favorite') + ': ' + title, 'aria-pressed': !!skill.favorite }, skill.favorite ? '★' : '☆')),
          h('p', { className: 'pw-purpose', title: text(skill.description) }, text(skill.description) || text(skill.whenToUse) || '—'),
          reason && h('p', { className: 'pw-help' }, text(reason)),
          h('div', { className: 'pw-card-foot' },
            h(Button, { className: 'pw-select-button', disabled: disabled || !skill.available || skill.status === 'retired', 'aria-label': t(picked ? 'selected' : 'select') + ': ' + title, 'aria-pressed': picked, onClick: () => chooseSkill(skill.id) }, picked ? '✓ ' + t('selected') : '+ ' + t('select')),
            h('span', { className: 'pw-rating-summary' }, Number(skill.averageRating) > 0 ? '★ ' + Number(skill.averageRating).toFixed(1) + ' · ' : '', (skill.reviewCount || 0) + ' ' + t('reviews'))),
          h('details', { className: 'pw-details' }, h('summary', null, t('details')),
            h('p', { className: 'pw-detail-id pw-muted' }, skill.id),
            h('label', { className: 'pw-check' }, h('input', { type: 'checkbox', checked: sessionAllowed, disabled: policyDisabled || (!sessionAllowed && !autoEligible), onChange: e => changeAllowlist(skill.id, e.target.checked) }), t('sessionAllow')),
            h('label', { className: 'pw-check' }, h('input', { type: 'checkbox', checked: defaultAllowed, disabled: policyDisabled || (!defaultAllowed && !autoEligible), onChange: e => changeAllowlist(skill.id, e.target.checked, true) }), t('defaultAllow')),
            !autoEligible && h('p', { className: 'pw-help' }, t('autoUnavailable')),
            h('div', { className: 'pw-badges' }, h('span', { className: 'pw-badge' }, t(skill.available ? 'available' : skill.current?.enabled === false ? 'disabled' : 'unavailable')), skill.category && h('span', { className: 'pw-badge' }, categoryLabel(skill.category)), h('span', { className: 'pw-badge' }, t(skill.status || 'testing'))),
            h('p', null, text(skill.description)), h('h4', { className: 'pw-card-title' }, t('when')), h('p', null, text(skill.whenToUse) || '—'),
            skill.platforms && h('p', { className: 'pw-muted' }, text(skill.platforms)), h('p', { className: 'pw-help' }, t('guidance')),
            skill.sideEffects && h('p', null, t('effects') + ': ' + text(skill.sideEffects)), h('p', null, t('source') + ': ' + (text(skill.source || skill.origin) || '—')),
            skill.provider && h('p', null, t('provider') + ': ' + text(skill.provider)),
            originalFields.length > 0 && h('details', null, h('summary', null, t('originalInfo')), originalFields.map(key => h('p', { key }, h('strong', null, t(key) + ': '), text(skill[key])))),
            h(Field, { label: t('status') }, h(Select, { label: t('status') + ': ' + title, value: skill.status || 'testing', onChange: status => setSkillStatus(skill, status), disabled: disabled || loading, options: STATUSES.map(value => ({ value, label: t(value) })) })), h('p', { className: 'pw-help' }, t('retiredHelp'))));
      }
      return h('section', { className: 'pw-root', 'aria-label': t('title') }, h('style', null, CSS),
        h('div', { className: 'pw-body' },
          h('header', { className: 'pw-header' }, h('div', null, h('div', { className: 'pw-row' }, h(Icon, { size: 21 }), h('h1', { className: 'pw-heading' }, t('title'))), h('p', { className: 'pw-subtitle' }, t('subtitle')))),
          h('div', { className: 'pw-builder' }, h('div', { className: 'pw-row pw-between' }, h('strong', null, t('manualMode')), h(Button, { role: 'switch', 'aria-checked': manualMode?.enabled === true, disabled: disabled || loading || !manualMode, onClick: () => updatePolicy('setManualMode', { enabled: !manualMode.enabled }, 'manualChanged') }, manualMode ? t(manualMode.enabled ? 'manualOn' : 'manualOff') : t('loading'))),
            h('p', { className: 'pw-help' }, t('manualHelp')),
            manualMode && h(React.Fragment, null,
              h('div', { className: 'pw-badges' }, h('span', { className: 'pw-badge' }, t('allowlistCount', { count: manualMode.allowlist.length })), h('span', { className: 'pw-badge' }, t('defaultAllowlistCount', { count: manualMode.defaultAllowlist.length }))),
              h('details', { className: 'pw-details' }, h('summary', null, t('allowlistManage')), renderAllowlist(), renderAllowlist(true), h('p', { className: 'pw-help' }, t('defaultAllowlistHelp'))))),
          notice && h('div', { className: 'pw-notice ' + (notice.error ? 'pw-notice-error' : 'pw-notice-success'), role: notice.error ? 'alert' : 'status' }, h('div', { className: 'pw-row pw-between' }, h('span', null, notice.text), h(Button, { quiet: true, onClick: () => setNotice(null), 'aria-label': t('close') }, '×')), notice.error && h(Button, { quiet: true, onClick: () => { if (connection === 'error') setConnectAttempt(value => value + 1); else void refresh(); }, disabled: !!busy }, t(connection === 'error' ? 'retry' : 'refresh'))),
          h('div', { className: 'pw-tabs', role: 'tablist', 'aria-label': t('title') }, tabs.map(value => h('button', {
            key: value, type: 'button', className: 'pw-tab', role: 'tab', disabled: !!busy, id: 'pw-tab-' + target + '-' + value, 'aria-selected': tab === value, 'aria-controls': 'pw-content-' + target + '-' + value, tabIndex: tab === value ? 0 : -1,
            onKeyDown: e => {
              if (activeOperation.current || !['ArrowLeft', 'ArrowRight', 'Home', 'End'].includes(e.key)) return;
              e.preventDefault();
              const next = e.key === 'Home' ? 0 : e.key === 'End' ? tabs.length - 1 : (tabs.indexOf(tab) + (e.key === 'ArrowRight' ? 1 : -1) + tabs.length) % tabs.length;
              setTab(tabs[next]); setQuery(''); e.currentTarget.parentNode.children[next].focus();
            }, onClick: () => { if (activeOperation.current) return; setTab(value); setQuery(''); },
          }, t(value === 'skills' ? 'allSkills' : value === 'history' ? 'shortHistory' : value)))),
          !target ? h('div', { className: 'pw-empty' }, t('noTarget')) : connection !== 'ready' ? h('div', { className: 'pw-empty', role: 'status' }, connection === 'loading' ? t('connecting') : t('error')) :
          h('section', { role: 'tabpanel', id: 'pw-content-' + target + '-' + tab, 'aria-labelledby': 'pw-tab-' + target + '-' + tab, 'aria-busy': loading || !!busy },
            busy && h('p', { className: 'pw-help', role: 'status' }, t('busy')),
            tab !== 'history' && h(React.Fragment, null,
              h('form', { className: 'pw-builder', onSubmit: useSkill },
                h(Field, { label: t('task') }, h('textarea', { className: 'pw-textarea', value: brief, onChange: e => { setBrief(e.target.value); setRecommendations(null); setUsageRecords([]); }, placeholder: t('taskPlaceholder'), disabled: !!busy, required: true })),
                h('div', { className: 'pw-row pw-between' }, h(Button, { disabled: disabled || !brief.trim(), onClick: recommendSkills }, t('recommend')), h('span', { className: 'pw-label' }, t(combination ? 'combination' : 'single')))),
              usageRecords.length > 0 && h('div', { 'aria-live': 'polite' }, h('h2', { className: 'pw-section-title' }, t('trials')), usageRecords.map(trial => renderTrial(trial, false))),
              combination && selected.length > 0 && h('details', { className: 'pw-builder', open: true }, h('summary', null, t('combinationSetup')),
                h('p', { className: 'pw-help' }, t('combinationHelp')),
                h(Field, { label: t('primarySkill') }, h(Select, { label: t('primarySkill'), value: primaryId, disabled: !!busy, onChange: value => { setPrimaryId(value); setUsageRecords([]); }, options: selected.map(id => ({ value: id, label: catalog.skills.find(skill => skill.id === id)?.title || id })) })),
                selected.includes(primaryId) && renderResponsibility(primaryId, t('primarySkill')),
                selected.length > 1 && h('h3', { className: 'pw-card-title' }, t('supportingSkills')),
                selected.filter(id => id !== primaryId).map((id, index, supporting) => h('div', { key: id }, renderResponsibility(id, t('supportingSkill', { count: index + 1 })),
                  h('div', { className: 'pw-card-foot' },
                    h(Button, { disabled: !!busy || index === 0, onClick: () => moveSupportingSkill(id, -1), 'aria-label': t('moveUp') + ': ' + (catalog.skills.find(skill => skill.id === id)?.title || id) }, t('moveUp')),
                    h(Button, { disabled: !!busy || index === supporting.length - 1, onClick: () => moveSupportingSkill(id, 1), 'aria-label': t('moveDown') + ': ' + (catalog.skills.find(skill => skill.id === id)?.title || id) }, t('moveDown')),
                    h(Button, { disabled: !!busy, onClick: () => chooseSkill(id), 'aria-label': t('remove') + ': ' + (catalog.skills.find(skill => skill.id === id)?.title || id) }, t('remove')))))),
              recommendations && h('section', { className: 'pw-builder', 'aria-label': t('recommendations'), 'aria-live': 'polite' }, h('h2', { className: 'pw-section-title' }, t('recommendations')), h('p', { className: 'pw-help' }, recommendations.notice || t('recommendationHelp')),
                recommendations.skills.length ? h('div', { className: 'pw-grid' }, recommendations.skills.map(row => renderSkill(catalog.skills.find(item => item.id === row.id) || row, row.reason))) : h('p', { className: 'pw-muted' }, t('recommendationEmpty'))),
              catalog.catalogComplete === false && h('p', { className: 'pw-notice', role: 'status' }, catalog.notice),
              h('div', { className: 'pw-filters' }, h('input', { className: 'pw-input', type: 'search', value: query, onChange: e => setQuery(e.target.value), placeholder: t('search'), 'aria-label': t('search') }),
                h('details', null, h('summary', null, t('filters') + (category || taskFilter || statusFilter || !availableOnly ? ' ·' : '')),
                  h('div', { className: 'pw-filter-grid' }, h(Select, { label: t('allCategories'), value: category, onChange: setCategory, options: options(categories, 'allCategories', categoryLabel) }), h(Select, { label: t('allTasks'), value: taskFilter, onChange: setTaskFilter, options: options(tasks, 'allTasks') }), h(Select, { label: t('allStates'), value: statusFilter, onChange: setStatusFilter, options: [{ value: '', label: t('allStates') }, ...STATUSES.map(value => ({ value, label: t(value) }))] })),
                  h('label', { className: 'pw-check' }, h('input', { type: 'checkbox', checked: availableOnly, onChange: e => setAvailableOnly(e.target.checked) }), t('availableOnly')))),
              loading && !catalog.skills.length ? h('div', { className: 'pw-empty', role: 'status' }, t('loading')) : visibleSkills.length ? h('div', { className: 'pw-grid' }, visibleSkills.map(skill => renderSkill(skill))) : h('div', { className: 'pw-empty' }, t('empty')),
              h('details', { className: 'pw-originals' }, h('summary', null, t('originals')), h('p', { className: 'pw-help' }, t('originalsHelp')),
                h('div', { className: 'pw-grid' }, originals.map(item => h('article', { key: item.id, className: 'pw-card' }, h('h3', { className: 'pw-card-title' }, item.title), h('p', { className: 'pw-muted' }, item.description), h('div', { className: 'pw-card-foot' }, h(Button, { disabled, onClick: () => activateOriginal(item) }, t(item.kind === 'web' ? 'openOriginal' : 'useOriginal')), item.id === 'youmind' && h(Button, { quiet: true, disabled, onClick: () => void operate('refreshLibrary', { action: 'refresh' }, undefined, t('libraryRefreshed')) }, t('refreshLibrary')))))),
                !loading && !originals.length && h('p', { className: 'pw-help' }, t('originalsUnavailable')))),
            tab === 'history' && h(React.Fragment, null, h('input', { className: 'pw-input', type: 'search', value: query, onChange: e => setQuery(e.target.value), placeholder: t('historySearch'), 'aria-label': t('historySearch') }), loading && !history.trials.length ? h('div', { className: 'pw-empty', role: 'status' }, t('loading')) : filteredTrials.length ? filteredTrials.map(trial => renderTrial(trial, true)) : h('div', { className: 'pw-empty' }, history.trials.length ? t('empty') : t('noHistory')))),
          h('details', { className: 'pw-toolbar' }, h('summary', null, t('more')), h('div', { className: 'pw-row' }, h(Button, { quiet: true, disabled: disabled || loading, onClick: () => void refresh() }, t('refresh')), h(Button, { quiet: true, disabled, onClick: () => void operate('export', { action: 'export' }, payload => { setExported(JSON.stringify(payload, null, 2)); }, t('exported')) }, t('export')))),
          exported && h('section', { className: 'pw-builder' }, h('div', { className: 'pw-row pw-between' }, h('h2', { className: 'pw-section-title' }, t('exportedState')), h(Button, { quiet: true, onClick: () => setExported('') }, t('close'))), h('textarea', { className: 'pw-prompt', readOnly: true, value: exported, 'aria-label': t('exportedState') }), h(Button, { onClick: () => void copy(exported) }, t('copy')))),
        target && connection === 'ready' && tab !== 'history' && h('footer', { className: 'pw-actionbar', 'aria-label': t('selectedSkills') },
          h('div', { className: 'pw-row pw-between' }, h('div', { className: 'pw-selection-summary' }, h('strong', { title: selectedTitles.join(' · ') }, selected.length ? selectedTitles.join(' · ') : t('selectedEmpty')), h('span', { className: 'pw-muted' }, t(combination ? 'selectedCount' : 'selectedSingle', { count: selected.length }))), h(Button, { quiet: true, disabled: !selected.length || !!busy, onClick: () => setSelected([]) }, t('clear'))),
          h('div', { className: 'pw-segmented', role: 'group', 'aria-label': t('mode') }, ['single', 'combination'].map(value => h(Button, { key: value, disabled: !!busy, 'aria-pressed': mode === value, onClick: () => changeMode(value) }, t(value)))),
          h('div', { className: 'pw-actions' }, combination ? h(Button, { primary: true, disabled: disabled || selected.length < 2 || !selected.includes(primaryId) || !brief.trim(), onClick: combineSkills }, t('shortCombine')) : h(Button, { primary: true, disabled: disabled || selected.length !== 1 || !brief.trim(), onClick: useSkill }, t('shortUse'))),
          h('p', { className: 'pw-help' }, t(!selected.length ? 'selectionHelp' : !brief.trim() ? 'briefRequired' : combination ? 'footerCombine' : 'footerSingle'))));
    }
    return {
      inject: ['remote.commands', 'remote', 'slots', 'locale', 'sessions', 'sidebarRight', 'sidebarRightTabs'],
      apply(ctx) {
        ctx.effect(() => ctx.locale.register(NS, { zh, en }), 'prompt-workbench: dictionaries');
        const t = ctx.locale.bind(NS);
        // The hook is UseProjection(key), supplied by the native Session scope.
        // Timestamp and tokens suppress persisted/replayed opens, including delayed baselines.
        const seenOpens = new Map();
        function HeaderEntry(props) {
          const request = props.useProjection('promptWorkbenchOpen');
          const mountedAt = React.useRef(Date.now());
          React.useEffect(() => {
            if (!request || typeof request.token !== 'string' || !Number.isFinite(request.time)) return;
            if (seenOpens.get(props.sessionId) === request.token) return;
            seenOpens.set(props.sessionId, request.token);
            if (request.time < mountedAt.current) return;
            ctx.sidebarRight.openTabIn(props.sessionId, PANEL);
          }, [props.sessionId, request]);
          return h(React.Fragment, null, h('style', null, CSS), h('button', { type: 'button', className: 'pw-header-entry', title: t('title'), 'aria-label': t('title'), onClick: () => ctx.sidebarRight.openTabIn(props.sessionId, PANEL) }, h(Icon, { size: 17 })));
        }
        ctx.effect(() => ctx.sidebarRightTabs.register({ id: PANEL, kind: PANEL, title: () => t('title'), keepMounted: true, guide: [{ id: PANEL, order: 8, title: () => t('title') }] }), 'prompt-workbench: tab type');
        ctx.slots.inject('sidebar.right.pane.tab', () => ctx.slots.register({ name: 'sidebar.right.pane.tab', key: PANEL, locale: NS }, props => h(Panel, { key: props.sessionId, ctx, t: props.t || t, sessionId: props.sessionId, inputActions: props.inputActions })));
        ctx.slots.inject('conversation.session.header.utilities', () => ctx.slots.register({ name: 'conversation.session.header.utilities', id: PANEL, order: 8, locale: NS }, props => h(HeaderEntry, { ...props, key: props.sessionId })));
      },
    };
  },
});
