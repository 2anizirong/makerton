document.getElementById("search-btn").addEventListener("click", function() {
    let input = document.getElementById("search").value;
    
    if (input) {
        // 검색한 장소를 서버에 전달
        fetch(`/save_search`, {
            method: "POST",
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ place: input })
        })
        .then(response => response.json())
        .then(data => {
            if (data.status === 'success') {
                // 장소가 존재하면 화재 대처 서비스 페이지로 이동
                window.location.href = "/fireservice";
            } else {
                // 장소가 없으면 알림창 표시
                alert("해당 장소는 저장되어 있지 않습니다.");
            }
        });
    } else {
        alert("장소를 입력하세요.");
    }
});
