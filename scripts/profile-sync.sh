#!/usr/bin/env bash
# Sets repository descriptions, topics and homepages so the pinned cards on the
# profile stop rendering as bare names, and aligns the profile bio with the README.
#
# Requires the GitHub CLI: winget install --id GitHub.cli
#   gh auth login
#   gh auth refresh -s user   # only needed for the bio/company step at the bottom
#
# Usage: bash scripts/profile-sync.sh

set -euo pipefail

repo_meta() {
  local repo="$1" desc="$2" home="$3"; shift 3
  echo "→ $repo"
  gh repo edit "Zebbb01/$repo" --description "$desc" ${home:+--homepage "$home"}
  if [ "$#" -gt 0 ]; then
    gh repo edit "Zebbb01/$repo" $(printf -- '--add-topic %s ' "$@")
  fi
}

repo_meta Portfolio \
  "Personal portfolio and case-study site — Next.js 16, Supabase, Framer Motion, with an AI live-chat widget" \
  "https://portfolio-five-ruddy-49.vercel.app" \
  nextjs typescript supabase portfolio framer-motion

repo_meta Workout-Tracker \
  "Body Tracker — offline-first fitness PWA with AI meal analysis from food photos" \
  "https://body-tracker-iota.vercel.app" \
  pwa nextjs typescript indexeddb ai supabase

repo_meta CashFlo \
  "Personal finance tracker with budgets, categorised spend and analytics" \
  "https://cash-flo-nine.vercel.app" \
  nextjs typescript supabase finance

repo_meta Salary-Management \
  "Payroll and salary management dashboard with role-based access" \
  "https://salary-management-kappa.vercel.app" \
  nextjs typescript dashboard payroll

repo_meta ai-chatbot-arnold \
  "Multi-provider AI chatbot — OpenAI, Anthropic and Azure behind one interface" \
  "" \
  ai openai anthropic nextjs typescript

repo_meta OSCA \
  "Civic platform for a senior citizen affairs office — records, benefits and reporting" \
  "" \
  nextjs prisma postgresql civic-tech

repo_meta Agright-NextJs \
  "Agriculture technology marketing site built with Next.js" \
  "" \
  nextjs typescript

repo_meta Zebbb01 \
  "Profile README — brand assets and the contribution snake workflow" \
  "" \
  profile-readme

# Profile bio and company, aligned with the README positioning.
# Needs the `user` scope: gh auth refresh -s user
gh api -X PATCH /user \
  -f bio="Software engineer — production SaaS, mobile apps and business automation. Currently building a BIR-compliant accounting platform." \
  -f company="Poseidon Distribution OPC" \
  -f blog="https://portfolio-five-ruddy-49.vercel.app" \
  -f location="Philippines"

echo
echo "Done. Pins are still manual: github.com/Zebbb01 → Customize your pins →"
echo "  Portfolio · Workout-Tracker · OSCA · CashFlo · Salary-Management"
