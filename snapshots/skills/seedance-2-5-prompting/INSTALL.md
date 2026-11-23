# Install this skill

This is Seedance 2.5 Prompting, the free skill from promptcraft.shop. Here is how to put it into Claude.

## Claude Code

Copy the `seedance-2-5-prompting` folder into your skills directory:

```
~/.claude/skills/seedance-2-5-prompting
```

Create the `skills` folder if it is not there. Restart Claude Code. The skill
loads on its own when your request matches it. You can also call it by name.

## Claude desktop and claude.ai

Upload the folder as a skill in your settings, under Capabilities, then
Skills. The whole folder goes up, not just `SKILL.md`, because the references
carry the templates and the examples.

## Check it worked

Ask Claude:

> Use seedance-2-5-prompting. A 20 second product film of a perfume bottle on wet stone.

You should get a prompt with a Generation Goal, stages that each end with an End state, an audio block and a Maintain Consistency block. If Claude writes a plain paragraph with no
structure, the skill did not load.

## What is in here

| File | What it holds |
|---|---|
| `SKILL.md` | The rules, the workflow and the sources |
| `references/camera-and-look-lock.md` | The locked look block, camera bodies, lenses, film stocks and grades |
| `references/editing-and-extension.md` | Editing a video, and extending it forward or backward |
| `references/keyframes-storyboards-blockouts.md` | First and last frames, keyframe sequences, storyboard grids, blockouts |
| `references/multi-reference-system.md` | Many characters, props and scenes: mapping, profiles, per-scene selection |
| `references/oneclick-and-transitions.md` | One-click video from images, and seamless transitions between clips |

## Licence

Free to use on your own and your clients' work. Please do not resell it or republish it as your own.

promptcraft.shop
