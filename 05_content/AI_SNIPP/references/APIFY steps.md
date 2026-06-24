# Instagram Niche Intelligence — Full Research + Content Agent
## OUTPUT FORMAT — CRITICAL INSTRUCTION
Do NOT output plain text or markdown. After completing all research phases below, compile ALL findings into a **single, well-structured PDF file** using Claude's artifact/file creation capability. The PDF must include:
- A cover page: account handle, niche, date generated
- A table of contents
- One clearly formatted section per phase (Phase 1, 2, 3, 4)
- All tables, lists, and scripts formatted professionally for printing/sharing
- Page numbers and section headers

Do not stream text output. Do not show intermediate results as plain text. Run all Apify scrapers silently, collect all data, then produce the final PDF artifact at the end.

---
## YOUR CONFIG
Handle: @ai_snipp
Niche: AI, tech, tools, AI tricks, AI learnings, AI tools
Audience: Software engineers, video editors, Claude users, AI users, tech, artificial intelligence,  AI learners, developers, AI explorer, AI enthusiast
Language: Hinglish (Hindi + English)
Goal: grow followers fast
Posting frequency: daily (7 posts/week)
Competitors: @thevarunmayya, @ezexplains, @cyborggirll, @thenawazshaikh, @trakin.ai
Subreddits: r/learnprogramming, r/artificial, r/ChatGPT, r/webdev, r/aitools, r/claudeai, r/softwareengineer, r/techindia, r/google ai, r/antigravity, r/chat gpt, r/gemini, r/open claw, r/harnes, r/ai agents, r/agentic ai
Hashtags: #aitools, #claudeai, #softwareengineer, #techindia, #google ai, #antigravity, #chat gpt, #gemini, #open claw, #harnes, #ai agents, #agentic ai
Research keywords: AI tools, Claude API, automation, software engineering, aitools, claudeai, softwareengineer, techindia, google ai, antigravity, chat gpt, gemini, open claw, harnes, ai agents, agentic ai
Content format mix: 50% Reels, 30% Carousels, 20% Static
Reel duration: 15–30 second reels
Hook style: tool demo with wow moment
Tone: storytelling and personal
Signature CTA: "DM me the word TOOLS and I'll send you the full list"
Stealing from competitors: hook formulas, CTA patterns, content formats, hashtag strategy, posting times

## APIFY ACTORS
- apify/instagram-profile-scraper → profiles + posts
- apify/instagram-comment-scraper → comment extraction
- breathtaking_anthem/instagram-hashtag-posts-scraper → hashtag top posts
- easyapi/reddit-comments-search-scraper → Reddit pain points

---

## PHASE 1 — PROFILE AUDIT

Run: apify/instagram-profile-scraper
Input: { "usernames": ["ai_snipp"] }

Analyse and return:

PROFILE METRICS:
- Follower count / following / post count
- Bio text + website link
- Engagement rate = (avg likes + avg comments) / followers × 100
- Avg likes per post / avg comments per post
- Posting frequency (posts per week based on latest 12 posts)

CONTENT BREAKDOWN (from latestPosts):
- % Reels vs Carousels vs Static images
- Average caption length (short <50 words / medium / long >150 words)
- Most used hashtag clusters
- Most common hook style in top captions

TOP 5 POSTS (sort by likes + comments):
For each: post URL, likes, comments, content type, caption opening line, hashtags used

CONTENT GAPS (compare my content vs niche topics):
List 5 topics common in the "AI, tech, tools, AI tricks, AI learnings, AI tools" niche that I have NOT posted about yet.
These gaps = my fastest growth opportunities.

## PHASE 2 — COMPETITOR INTELLIGENCE

Run: apify/instagram-profile-scraper
Input: { "usernames": ["thevarunmayya", "ezexplains", "cyborggirll", "thenawazshaikh", "trakin.ai"] }

For EACH competitor extract:
1. Followers + engagement rate
2. Content format split (reels/carousels/static %)
3. Posting frequency
4. Top 5 posts (likes + comments) → save their URLs
5. Caption hook patterns (first 10 words of top posts)
6. CTA they use most
7. Hashtag count per post

COMMENT EXTRACTION (for competitor intelligence):
For each competitor's top 3 posts, run: apify/instagram-comment-scraper
Input: { "directUrls": [TOP_3_POST_URLS_PER_COMPETITOR], "resultsLimit": 100 }

From comments classify into 4 buckets:
BUCKET A — Questions: comments ending in "?" or starting with "how", "what", "where", "when", "why", "can you"
BUCKET B — Requests: "can you make a video on", "next video should be", "please cover", "I'd love to see"
BUCKET C — Frustrations: contains "wish", "confusing", "doesn't work", "nobody explains", "I've been trying"
BUCKET D — Praise: what specific thing do they compliment? ("love how you", "finally someone who", "this is exactly")

STEAL ANALYSIS — extract specifically: hook formulas, CTA patterns, content formats, hashtag strategy, posting times

CROSS-COMPETITOR SYNTHESIS:
1. Which content format gets highest engagement across all competitors?
2. Top 3 topics that consistently outperform their average
3. Which hook formulas appear in their top 10% of posts?
4. THE GAP: What does your audience complain about / ask for that NONE of these competitors cover well?

Output: Comparison table + ranked list of 10 insights from comment buckets.

## PHASE 3 — AUDIENCE PAIN POINT MINING

### 3A — Instagram Comment Mining

Step 1: Run breathtaking_anthem/instagram-hashtag-posts-scraper
Input: { "hashtags": ["aitools", "claudeai", "softwareengineer", "techindia", "google ai", "antigravity", "chat gpt", "gemini", "open claw", "harnes", "ai agents", "agentic ai"], "resultsPerHashtag": 10 }
→ Collect top 10 post URLs per hashtag (up to 120 URLs total)

Step 2: Run apify/instagram-comment-scraper on collected URLs
Input: { "directUrls": [UP_TO_20_URLS_FROM_STEP_1], "resultsLimit": 150 }

PAIN LANGUAGE FILTER — extract comments containing ANY of:
Frustration: "struggling", "can't figure out", "so confusing", "doesn't work", "waste of time", "nobody tells you", "I wish someone"
Questions: any comment ending in "?" with 5+ words
Desire: "I need", "looking for", "wish there was", "is there a way to", "does anyone know how"
Requests: "can someone explain", "please make a video", "what tool do you use"

### 3B — Reddit Mining

Run: easyapi/reddit-comments-search-scraper
Input:
{
  "searchTerms": [
    "AI tools problems",
    "AI tools struggling",
    "AI tools best tools",
    "Software engineers frustration",
    "how to AI tools",
    "Claude API beginner mistakes"
  ],
  "subreddits": ["learnprogramming", "artificial", "ChatGPT", "webdev", "aitools", "claudeai", "softwareengineer", "techindia", "google ai", "antigravity", "chat gpt", "gemini", "open claw", "harnes", "ai agents", "agentic ai"],
  "maxItems": 100,
  "sort": "top"
}

Extract ONLY comments with score > 5. Classify same as above buckets.

PAIN POINT DATABASE — compile final output:
1. Top 10 pain points ranked by frequency (Reddit + Instagram combined)
   Format: [Pain point] | [Frequency] | [Source: Reddit/Instagram/Both] | [Example quote verbatim]
2. Top 5 most-asked questions (exact wording from real comments)
3. TOP HOOK PHRASES — 10 exact emotional phrases from real comments to use as reel hooks
4. 3 underserved topics: problems asked repeatedly with zero good answers in the niche
5. Viral content formula: analyse the most-liked posts in hashtag scrape → what structure do they follow?

## PHASE 4 — 30-DAY REEL SCRIPTS + CONTENT CALENDAR

Using ALL data from phases above, create a 30-day content calendar + full reel scripts for @ai_snipp.

RULES:
- Language: Hinglish (Hindi + English)
- Format mix: 50% Reels, 30% Carousels, 20% Static
- Reel length: 15–30 second reels
- Hook style: tool demo with wow moment
- Tone: storytelling and personal
- Goal: grow followers fast
- Every post must directly address a pain point from Phase 3
- Hooks must use REAL language extracted from comments — not generic
- Signature CTA on every post: "DM me the word TOOLS and I'll send you the full list"

WEEKLY THEMES:
Week 1 (Days 1–7): AWARENESS — "You're not alone. Here's why this is hard."
  → Posts that name the pain loudly. Make audience feel seen. Heavy on relatability.
Week 2 (Days 8–14): EDUCATION — "Here's exactly how to fix it."
  → Step-by-step tutorials, tool explainers, how-tos. Build authority.
Week 3 (Days 15–21): PROOF — "Here's what's possible."
  → Results, before/after, case studies, transformations. Build desire.
Week 4 (Days 22–30): ENGAGEMENT — "What do you think?"
  → Debates, polls, controversial opinions, viral questions. Grow comments.

FOR EACH OF THE 30 DAYS OUTPUT THIS EXACT FORMAT:

════════════════════════════════
DAY [N] · [DD MMM] · [FORMAT: Reel/Carousel/Static]
════════════════════════════════
TOPIC: [specific, researched topic]
PAIN POINT: [which pain point from Phase 3 this targets]
HOOK SOURCE: [exact quote from real comment that inspired the hook]

HOOK (first 3 seconds — say this verbatim):
"[exact hook line — use real comment language, create curiosity or shock]"

REEL SCRIPT (15–30 second reels):
[0–3s]  HOOK: [exact words to say on camera]
[3–8s]  AGITATE: [deepen the pain — make them feel it]
[8–20s] INSIGHT: [the one thing they didn't know — your value bomb]
[20–30s] PROOF: [quick stat / example / before-after / tool demo moment]
[Last 3s] CTA: "DM me the word TOOLS and I'll send you the full list"

CAPTION (paste this):
[Hook line repeated]
[2–3 lines expanding on the insight]
[1 line of social proof or urgency]
DM me the word TOOLS and I'll send you the full list
.
.
.
[10 hashtags from Phase 3 research]

THUMBNAIL TEXT: [3–5 word text overlay for the reel cover]
MODEL AFTER: [which competitor post format to reference]
BEST POSTING TIME: [based on competitor engagement patterns]
VIRAL POTENTIAL: [Low / Medium / High ⚡]
════════════════════════════════

AFTER THE CALENDAR OUTPUT:

A/B TEST HOOKS — Top 5 hooks to test first (pick these for Week 1):
For each: Hook text | Why it will work | Which pain point | Expected emotion triggered

⚡ HIGH-PROBABILITY VIRAL POSTS — mark 3 posts most likely to blow up and explain:
- Why this topic is primed to go viral right now
- Which competitor's comment section proves the demand
- What makes the hook irresistible

CONTENT BATCHING PLAN:
Group the 30 posts into filming sessions. Tell me which 5–7 to film together and why.

HASHTAG STRATEGY:
Based on Phase 3 data, create 3 hashtag sets:
- Set A (broad reach): [10 hashtags]
- Set B (niche authority): [10 hashtags]  
- Set C (engagement bait): [10 hashtags]
Rotate between sets across the 30 days.

---
## EXECUTION ORDER
1. Run Phase 1 scraper → analyse profile → note content gaps
2. Run Phase 2 scrapers → extract competitor comments → identify gap + steal list
3. Run Phase 3 scrapers (hashtags + Reddit) → build pain point database with real quotes
4. Use ALL scraped data to power Phase 4 — every hook, script, and CTA must trace back to a real comment or post from the research

IMPORTANT: Do not use generic advice. Every hook must come from real comment language. Every topic must be validated by search volume in Phase 3. Every CTA must align with the goal: grow followers fast.

---
## FINAL DELIVERABLE — PDF ONLY
Once all 4 phases are complete, compile everything into a single PDF artifact:
- No plain text output
- No markdown blocks shown in chat
- Just one downloadable PDF report with all research, tables, 30-day calendar, and full reel scripts
- PDF filename: instagram-intelligence-ai_snipp.pdf