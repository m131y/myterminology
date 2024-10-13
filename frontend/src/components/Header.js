document.addEventListener('DOMContentLoaded', function() {
    // 메뉴 토글 버튼과 메뉴 래퍼 선택
    const menuToggler = document.querySelector('.header-toggler');
    const menuWrapper = document.querySelector('.header-menu-wrapper');
    const menuText = menuToggler.querySelector('span');

    // 메뉴 상태 확인 변수
    let menuOpen = false;

    // 메뉴 토글 버튼 클릭 시 동작
    menuToggler.addEventListener('click', function() {
        if (menuOpen) {
            // 메뉴 닫기
            menuWrapper.style.height = '0'; // 메뉴를 접음
            menuWrapper.style.overflow = 'hidden'; // 스크롤 방지
            menuWrapper.style.pointerEvents = 'none'; // 클릭 방지
            menuText.textContent = 'Menu'; // 'CLOSE' -> 'MENU'로 변경
            menuOpen = false;
        } else {
            // 메뉴 열기
            menuWrapper.style.height = 'auto'; // 메뉴 펼침
            menuWrapper.style.overflow = 'visible'; // 스크롤 허용
            menuWrapper.style.pointerEvents = 'auto'; // 클릭 허용
            menuText.textContent = 'Close'; // 'MENU' -> 'CLOSE'로 변경
            menuOpen = true;
        }
    });
});
