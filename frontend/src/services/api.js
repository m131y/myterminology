import axios from 'axios';


export const postUrlAndGetNews = async (url) => {
    try {
        const response = await axios.post('/crw/process-news/', JSON.stringify({ url }), {
            headers: {
                'Content-Type': 'application/json', // Ensure correct content type for JSON
                'X-CSRFToken': getCookie('csrftoken'), // CSRF token header
            }
        });
        return response.data;
    } catch (error) {
        console.error('Error making the post request:', error);
        return { success: false, message: 'Network error or server is down' };
    }
}


function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}