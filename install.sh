#!/bin/bash

# Food Truck CLI Installation Script
# Script de instalação do Food Truck CLI

set -e

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚚 Configurando Food Truck CLI...${NC}"

# Get the current directory (where this script is located)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"

# Check if UV is installed
if ! command -v uv &> /dev/null; then
    echo -e "${RED}❌ UV não está instalado. Instale em: https://docs.astral.sh/uv/getting-started/installation/${NC}"
    exit 1
fi

# Create a wrapper script
WRAPPER_SCRIPT="$SCRIPT_DIR/foodtruck"
cat > "$WRAPPER_SCRIPT" << 'EOF'
#!/bin/bash
# Wrapper script for foodtruck CLI
cd "$(dirname "$0")"
uv run foodtruck "$@"
EOF

# Make the wrapper script executable
chmod +x "$WRAPPER_SCRIPT"
echo -e "${GREEN}✅ Script wrapper criado${NC}"

# Detect shell and add to PATH
SHELL_CONFIG=""
if [[ "$SHELL" == *"zsh"* ]]; then
    SHELL_CONFIG="$HOME/.zshrc"
    SHELL_NAME="zsh"
elif [[ "$SHELL" == *"bash"* ]]; then
    SHELL_CONFIG="$HOME/.bashrc"
    SHELL_NAME="bash"
else
    echo -e "${YELLOW}⚠️  Shell não detectado. Adicione manualmente ao seu arquivo de configuração:${NC}"
    echo -e "export PATH=\"$SCRIPT_DIR:\$PATH\""
    exit 1
fi

echo -e "${BLUE}📝 Configurando $SHELL_NAME...${NC}"

# Check if PATH is already set
if grep -q "export PATH.*$SCRIPT_DIR" "$SHELL_CONFIG" 2>/dev/null; then
    echo -e "${YELLOW}⚠️  PATH já configurado em $SHELL_CONFIG${NC}"
else
    # Add to shell configuration
    echo "" >> "$SHELL_CONFIG"
    echo "# Food Truck CLI" >> "$SHELL_CONFIG"
    echo "export PATH=\"$SCRIPT_DIR:\$PATH\"" >> "$SHELL_CONFIG"
    echo -e "${GREEN}✅ Adicionado ao $SHELL_CONFIG${NC}"
fi

# Install the package
echo -e "${BLUE}📦 Instalando pacote...${NC}"
uv pip install -e . > /dev/null 2>&1

echo -e "${GREEN}🎉 Instalação concluída!${NC}"
echo -e "${YELLOW}💡 Recarregue seu terminal ou execute:${NC}"
echo -e "source $SHELL_CONFIG"
echo -e ""
echo -e "${GREEN}🚀 Use o CLI com:${NC}"
echo -e "foodtruck"
echo -e ""
echo -e "${BLUE}🔧 Para desenvolvimento:${NC}"
echo -e "uv run task cli"
