
# 🐤 Jogo do Pica-Pau - Flappy Bird com Python e OpenGL

Este é um jogo desenvolvido em Python utilizando a biblioteca OpenGL (via PyOpenGL) e GLFW, inspirado no clássico Flappy Bird. O personagem principal é o Pica-Pau (Woody Woodpecker), que deve desviar de obstáculos, coletar itens e sobreviver o máximo possível.

---

## 🎮 Funcionalidades

- ✅ **Movimentação do Pica-Pau** com gravidade e pulo.
- 🌲 **Geração de obstáculos** (troncos) aleatórios.
- ❤️ **Sistema de vidas** visível na tela (até 7 vidas).
- 🧠 **Detecção de colisões** com margem de tolerância.
- ✨ **Itens especiais**:
  - `Vida` → Recupera uma vida.
  - `Urubu` → Tira uma vida.
  - `Invencibilidade` → Imunidade temporária (com efeito de piscar).
- 🧮 **Sistema de pontuação**.
- 💀 **Tela de Game Over** com score final.
- 🎨 **Texturas personalizadas** para o personagem e itens.
- 🕹️ **Controles simples e diretos**.

---

## 🧠 Lógica do Jogo

- A gravidade afeta constantemente o personagem.
- A cada certo tempo, obstáculos (troncos) são gerados na tela e se movem da direita para a esquerda.
- Se o personagem colidir com obstáculos, teto ou chão, ele perde uma vida.
- Após cada hit, o personagem fica piscando e **invulnerável por 1 segundo**.
- O jogo termina quando o jogador perde todas as vidas.

## 🛠️ Tecnologias Utilizadas

- **Python 3**
- **PyOpenGL** (renderização gráfica)
- **GLFW** (janela e controle de input)
- **Pillow** (carregamento de texturas)
- **Pygame** (renderização de texto com fonte personalizada)
- **Numpy** (manipulação de imagens)
---

## 🕹️ Controles

- **Barra de Espaço** → Faz o Pica-Pau pular.

---

## 🗂️ Estrutura do Código

- `WoodyWoodpeckerGame`: classe principal que gerencia o jogo.
- `load_texture()` – Carrega as texturas a partir de imagens PNG.
- `update_game_state()`: atualiza posições, obstáculos, itens e lógica de jogo.
- `check_collisions()`: detecta colisões com obstáculos e objetos.
- `draw_*()`: funções para renderizar elementos do jogo (personagem, vidas, itens...).
- `register_hit()` – Aplica dano ao personagem e ativa o timer de invulnerabilidade.
- `run()`: loop principal do jogo.
- `show_game_over()`: exibe a tela de Game Over com o score final.

---

## 📌 Créditos

Projeto acadêmico de Gustavo Muller, Luiz Fernando e Rafael Deboer  feito com Python + OpenGL.  
Personagem inspirado no Woody Woodpecker(Pica-Pau), da Universal Studios.
