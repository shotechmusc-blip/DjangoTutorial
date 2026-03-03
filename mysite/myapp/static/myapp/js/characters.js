/**
 * 擬人化キャラクターページ制御
 *
 * 方針:
 * - キャラクター解放判定はサーバー(Django)側の Stamp データのみを使用
 * - クライアント側では表示状態を変更しない
 * - このJSはスクロールヒントの制御のみ担当
 */

class CharacterPageManager {
  constructor() {
    this.wrapper = document.getElementById('charactersWrapper');
    this.scrollHint = document.getElementById('scrollHint');
  }

  setupScrolling() {
    if (!this.wrapper || !this.scrollHint) return;

    this.wrapper.addEventListener('scroll', () => {
      if (this.wrapper.scrollTop > 50) {
        this.scrollHint.classList.add('hide');
      } else {
        this.scrollHint.classList.remove('hide');
      }
    });
  }
}

function initializeCharacterPage() {
  const pageManager = new CharacterPageManager();
  pageManager.setupScrolling();
}

if (document.readyState === 'loading') {
  document.addEventListener('DOMContentLoaded', initializeCharacterPage);
} else {
  initializeCharacterPage();
}
