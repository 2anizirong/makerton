const API_KEY = 'AIzaSyDJOqiFGYBKSbMqdzc2y_CqjWnVrQmzxaw';  // Google Cloud Console에서 발급받은 YouTube API 키
const query = 'fire safety';  // 화재 관련 검색어
const maxResults = 2;  // 불러올 동영상 개수

// YouTube Data API를 사용해 동영상 검색
fetch(`https://www.googleapis.com/youtube/v3/search?part=snippet&type=video&q=${query}&maxResults=${maxResults}&key=${API_KEY}`)
    .then(response => response.json())
    .then(data => {
        const videos = data.items;
        const videoContainer = document.getElementById('youtube-videos');

        // 동영상 2개를 화면에 표시
        videos.forEach(video => {
            const videoId = video.id.videoId;

            const iframe = document.createElement('iframe');
            iframe.width = '300';
            iframe.height = '200';
            iframe.src = `https://www.youtube.com/embed/${videoId}`;
            iframe.frameBorder = '0';
            iframe.allow = 'accelerometer; autoplay; clipboard-write; encrypted-media; gyroscope; picture-in-picture';
            iframe.allowFullscreen = true;

            videoContainer.appendChild(iframe);
        });
    })
    .catch(error => console.error('Error fetching YouTube videos:', error));