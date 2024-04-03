function getSentiment(event, text) {
    if (!text || event.key !== "Enter") {
        answer.innerHTML = '';
        return;
    }
    // Sichtbarkeit wechseln
    answerPart.style.visibility = "visible";
    
    // Get Sentiment: Fetch API
    fetch('/sentiment?' + new URLSearchParams({
        text: text,
    }), {
        method: 'GET',
        headers: {}
    }).then(
        response => {
            console.log(response)
            response.text().then(function (text) {
                answer.innerHTML = text; // Text zuweisen
            });
        }
    ).then(
        success => console.log(success)
    ).catch(
        error => console.log(error)
    );



}