document.addEventListener('DOMContentLoaded', function() {
    const giftField = document.getElementById('gift-field');
    const openedCount = document.getElementById('opened-count');
    const remainingCount = document.getElementById('remaining-count');
    const message = document.getElementById('message');
    const result = document.getElementById('result');
    const giftImage = document.getElementById('gift-image');
    const congratulation = document.getElementById('congratulation');
    
    let openedBoxes = [];
    
    loadState();
    
    document.querySelectorAll('.gift-box:not(.opened)').forEach(box => {
        box.addEventListener('click', handleBoxClick);
    });
    
    function loadState() {
        fetch('/lab9/state')
            .then(response => response.json())
            .then(data => {
                openedBoxes = data.opened_boxes || [];
                updateCounters(data.opened_count, data.remaining_count);
                
                updateBoxesAppearance();
            })
            .catch(error => {
                console.error('Ошибка загрузки состояния:', error);
                showMessage('Ошибка загрузки состояния', 'error');
            });
    }
    
    function updateBoxesAppearance() {
        document.querySelectorAll('.gift-box').forEach(box => {
            const boxId = parseInt(box.dataset.boxId);
            
            if (openedBoxes.includes(boxId)) {
                box.classList.add('opened');
                box.style.cursor = 'default';
                box.removeEventListener('click', handleBoxClick);
            } else {
                box.classList.remove('opened');
                box.style.cursor = 'pointer';
                
                box.removeEventListener('click', handleBoxClick);
                box.addEventListener('click', handleBoxClick);
            }
        });
    }
    
    function handleBoxClick(event) {
        const box = event.currentTarget;
        const boxId = parseInt(box.dataset.boxId);
        
        openBox(boxId);
    }
    
    function openBox(boxId) {
        const box = document.querySelector(`.gift-box[data-box-id="${boxId}"]`);
        box.style.transform = 'scale(0.95)';
        
        fetch('/lab9/open_box', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ box_id: boxId })
        })
        .then(response => response.json())
        .then(data => {
            box.style.transform = '';
            
            if (data.success) {
                openedBoxes.push(boxId);
                
                updateCounters(data.opened_count, data.remaining_count);
                
                box.classList.add('opened');
                box.style.cursor = 'default';
                box.removeEventListener('click', handleBoxClick);
                
                showGift(data.gift_image, data.congratulation);
                
                showMessage(data.message, 'success');
                
                setTimeout(() => {
                    result.scrollIntoView({ behavior: 'smooth', block: 'center' });
                }, 300);
            } else {
                showMessage(data.message, 'error');
            }
        })
        .catch(error => {
            console.error('Ошибка открытия коробки:', error);
            showMessage('Ошибка соединения с сервером', 'error');
            box.style.transform = '';
        });
    }
    
    function updateCounters(opened, remaining) {
        openedCount.textContent = opened;
        remainingCount.textContent = remaining;
    }
    
    function showGift(giftImageUrl, congratulationText) {
        giftImage.src = giftImageUrl;
        congratulation.textContent = congratulationText;
        result.style.display = 'block';
    }
    
    function showMessage(text, type) {
        message.textContent = text;
        message.className = 'message ' + type;
        
        setTimeout(() => {
            if (message.textContent === text) {
                message.textContent = '';
                message.className = 'message';
            }
        }, 3000);
    }
});
