#!/usr/bin/env bash
# ==============================================================================
# create_jules_issue.sh
# ------------------------------------------------------------------------------
# Create a GitHub Issue for tasks or designs, attaching the latest open
# milestone and the 'jules' label for automated execution by Jules.
# ==============================================================================

set -euo pipefail

# Automatically retrieve repository information
REPO_SLUG=$(gh repo view --json nameWithOwner -q .nameWithOwner 2>/dev/null || echo "")

if [ -z "$REPO_SLUG" ]; then
  echo "❌ Error: Failed to run gh repo view in the current directory. Please run inside a Git repository."
  exit 1
fi

# Retrieve the latest open milestone (sorted by created_at)
MILESTONE_TITLE=$(gh api "repos/${REPO_SLUG}/milestones?state=open" --jq 'sort_by(.created_at) | last | .title' 2>/dev/null || echo "")

if [ -z "$MILESTONE_TITLE" ]; then
  echo "⚠️ Warning: No open milestone found. Proceeding without a milestone."
fi

TITLE=""
BODY=""
BODY_FILE=""

# Parse arguments
while [[ $# -gt 0 ]]; do
  case $1 in
    -t|--title)
      TITLE="$2"
      shift 2
      ;;
    -b|--body)
      BODY="$2"
      shift 2
      ;;
    -f|--file)
      BODY_FILE="$2"
      shift 2
      ;;
    -m|--milestone)
      MILESTONE_TITLE="$2"
      shift 2
      ;;
    -h|--help)
      echo "Usage: $0 [options]"
      echo "Options:"
      echo "  -t, --title <title>          Issue title"
      echo "  -b, --body <body>            Issue body (inline text)"
      echo "  -f, --file <path>            Issue body file (e.g. design.md)"
      echo "  -m, --milestone <name>       Milestone name (default: latest open milestone)"
      exit 0
      ;;
    *)
      if [ -z "$TITLE" ]; then
        TITLE="$1"
      else
        BODY="$1"
      fi
      shift
      ;;
  esac
done

if [ -z "$TITLE" ]; then
  echo -n "📝 Enter issue title: "
  read -r TITLE
fi

if [ -z "$BODY" ] && [ -z "$BODY_FILE" ]; then
  if [ -f "design.md" ]; then
    echo "💡 Found 'design.md' in current directory, using it as issue body."
    BODY_FILE="design.md"
  else
    echo -n "📝 Enter issue body: "
    read -r BODY
  fi
fi

# Build command
CMD=(gh issue create --repo "$REPO_SLUG" --title "$TITLE" --label "jules")

if [ -n "$MILESTONE_TITLE" ]; then
  CMD+=(--milestone "$MILESTONE_TITLE")
fi

if [ -n "$BODY_FILE" ] && [ -f "$BODY_FILE" ]; then
  CMD+=(--body-file "$BODY_FILE")
elif [ -n "$BODY" ]; then
  CMD+=(--body "$BODY")
fi

echo "🚀 Creating GitHub Issue..."
echo "  • Repository: $REPO_SLUG"
echo "  • Title: $TITLE"
[ -n "$MILESTONE_TITLE" ] && echo "  • Milestone: $MILESTONE_TITLE"
echo "  • Label: jules"

ISSUE_URL=$("${CMD[@]}")

echo ""
echo "🎉 Issue created successfully!"
echo "🔗 Issue URL: $ISSUE_URL"
echo "🤖 Jules will detect this issue and start implementation automatically."
