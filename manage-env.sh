#!/bin/bash

# manage-env.sh - AI Skill Environment Sync
# Synchronizes local project skills with global AI agent configurations.
# Focus: Gemini CLI, Antigravity, Claude Code, and GitHub Copilot CLI.

set -e

PROJECT_PATH=$(pwd)
SKILLS_PATH="${PROJECT_PATH}/skills"
ANTI_PATH="${PROJECT_PATH}/antigravity"

GEMINI_CONFIG="${HOME}/.gemini/settings.json"
CLAUDE_CONFIG="${HOME}/.claude/settings.json"
COPILOT_DIR="${PROJECT_PATH}/.github"
COPILOT_FILE="${COPILOT_DIR}/copilot-instructions.md"

# Help Message
usage() {
    echo "Usage: $0 [action] [tool]"
    echo ""
    echo "Actions:"
    echo "  --install      Add project skills to AI agent configurations"
    echo "  --uninstall    Remove project skills from AI agent configurations"
    echo ""
    echo "Tools:"
    echo "  gemini         Sync Gemini CLI / Antigravity (via settings.json)"
    echo "  claude         Sync Claude Code (via additionalDirectories)"
    echo "  copilot        Sync GitHub Copilot CLI (via .github instructions)"
    echo "  all            Sync all tools (default)"
    echo ""
    exit 1
}

# Check for jq
check_jq() {
    if ! command -v jq &> /dev/null; then
        echo "Error: 'jq' is required but not installed. Please install it to continue."
        exit 1
    fi
}

# Backup configuration files
backup_file() {
    local file=$1
    if [[ -f "$file" ]]; then
        cp "$file" "${file}.bak"
        echo "Backed up $(basename "$file") to $(basename "$file").bak"
    fi
}

# --- Gemini Logic ---
install_gemini() {
    echo "🔄 Syncing Gemini / Antigravity..."
    check_jq
    mkdir -p "$(dirname "$GEMINI_CONFIG")"
    if [[ ! -f "$GEMINI_CONFIG" ]]; then echo "{}" > "$GEMINI_CONFIG"; fi
    backup_file "$GEMINI_CONFIG"

    # Add paths to skills.paths and ensure uniqueness
    tmp_file=$(mktemp)
    jq --arg skills "$SKILLS_PATH" --arg anti "$ANTI_PATH" \
       '.skills.paths = ((.skills.paths // []) + [$skills, $anti] | unique)' \
       "$GEMINI_CONFIG" > "$tmp_file" && mv "$tmp_file" "$GEMINI_CONFIG"
    echo "✅ Gemini configuration updated."
}

uninstall_gemini() {
    echo "🗑️ Removing Gemini / Antigravity sync..."
    check_jq
    if [[ -f "$GEMINI_CONFIG" ]]; then
        tmp_file=$(mktemp)
        jq --arg skills "$SKILLS_PATH" --arg anti "$ANTI_PATH" \
           '.skills.paths |= map(select(. != $skills and . != $anti))' \
           "$GEMINI_CONFIG" > "$tmp_file" && mv "$tmp_file" "$GEMINI_CONFIG"
        echo "✅ Gemini configuration cleaned."
    fi
}

# --- Claude Logic ---
install_claude() {
    echo "🔄 Syncing Claude Code..."
    check_jq
    mkdir -p "$(dirname "$CLAUDE_CONFIG")"
    if [[ ! -f "$CLAUDE_CONFIG" ]]; then echo "{}" > "$CLAUDE_CONFIG"; fi
    backup_file "$CLAUDE_CONFIG"

    # Add project path to permissions.additionalDirectories
    tmp_file=$(mktemp)
    jq --arg path "$PROJECT_PATH" \
       '.permissions.additionalDirectories = ((.permissions.additionalDirectories // []) + [$path] | unique)' \
       "$CLAUDE_CONFIG" > "$tmp_file" && mv "$tmp_file" "$CLAUDE_CONFIG"
    
    # Ensure project root .clauderc exists if possible
    if [[ -d "${PROJECT_PATH}/claude" && ! -f "${PROJECT_PATH}/.clauderc" ]]; then
        echo "💡 Tip: Claude Code finds .clauderc in the project root. You may want to copy ./claude/.clauderc to the root."
    fi
    echo "✅ Claude configuration updated."
}

uninstall_claude() {
    echo "🗑️ Removing Claude Code sync..."
    check_jq
    if [[ -f "$CLAUDE_CONFIG" ]]; then
        tmp_file=$(mktemp)
        jq --arg path "$PROJECT_PATH" \
           '.permissions.additionalDirectories |= map(select(. != $path))' \
           "$CLAUDE_CONFIG" > "$tmp_file" && mv "$tmp_file" "$CLAUDE_CONFIG"
        echo "✅ Claude configuration cleaned."
    fi
}

# --- Copilot Logic ---
install_copilot() {
    echo "🔄 Syncing GitHub Copilot CLI..."
    mkdir -p "$COPILOT_DIR"
    
    local marker="# AI_SKILL_SYNC_MARKER"
    local content="See project-local skills in: $SKILLS_PATH"

    if [[ -f "$COPILOT_FILE" ]]; then
        if grep -q "$marker" "$COPILOT_FILE"; then
            echo "ℹ️ Copilot instructions already synced."
        else
            echo -e "\n$marker\n$content" >> "$COPILOT_FILE"
            echo "✅ Added sync reference to $COPILOT_FILE"
        fi
    else
        echo -e "$marker\n$content" > "$COPILOT_FILE"
        echo "✅ Created $COPILOT_FILE with sync reference."
    fi
}

uninstall_copilot() {
    echo "🗑️ Removing Copilot CLI sync..."
    if [[ -f "$COPILOT_FILE" ]]; then
        # Remove the marker and the line immediately following it
        sed -i '' '/# AI_SKILL_SYNC_MARKER/,+1d' "$COPILOT_FILE"
        echo "✅ Copilot instructions cleaned."
    fi
}

# Parse Arguments
ACTION=$1
TOOL=${2:-all}

if [[ "$ACTION" != "--install" && "$ACTION" != "--uninstall" ]]; then
    usage
fi

case "$TOOL" in
    gemini)
        [[ "$ACTION" == "--install" ]] && install_gemini || uninstall_gemini
        ;;
    claude)
        [[ "$ACTION" == "--install" ]] && install_claude || uninstall_claude
        ;;
    copilot)
        [[ "$ACTION" == "--install" ]] && install_copilot || uninstall_copilot
        ;;
    all)
        if [[ "$ACTION" == "--install" ]]; then
            install_gemini
            install_claude
            install_copilot
        else
            uninstall_gemini
            uninstall_claude
            uninstall_copilot
        fi
        ;;
    *)
        usage
        ;;
esac

echo "✨ Done."
