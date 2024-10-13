import React, { useState } from 'react';
import axios from 'axios';
import { useHistory } from 'react-router-dom';

function News() {
    const [url, setUrl] = useState('');
    const history = useHistory();

    const handleSubmit = async (event) => {
        event.preventDefault();
        try {
            const response = await axios.post('/crw/process-news/', { url }, {
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCookie('csrftoken')
                }
            });
            if (response.data.success) {
                history.push('/news');  // Redirect to news.html page
            } else {
                alert(response.data.message);  // Show error message if something goes wrong
            }
        } catch (error) {
            alert('Network error or server is down');
        }
    };

    return (
        <form onSubmit={handleSubmit}>
            <label>
                URL:
                <input 
                    type="text" 
                    value={url} 
                    onChange={e => setUrl(e.target.value)} 
                    placeholder="Enter the news URL"
                />
            </label>
            <button type="submit">Submit</button>
        </form>
    );
}

export default News;

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
