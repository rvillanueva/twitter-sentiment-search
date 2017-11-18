class MainController {
  constructor(){
    this.tweets = [];
  }
  init(){
    this.addEventListeners();
  }
  addEventListeners(){
    $('#include-rt-checkbox').change(() => {
      this.renderTweets();
    });
  }
  search(input){
    var term = input || $('#search-input').val();
    if(!term){
      console.error('No search term provided.')
      return;
    }
    console.log('Searching for ' + term);
    this.setSearchDisabled(true);
    this.getPosts(term)
    .then(res => {
      this.setSearchDisabled(false);
      console.log(res);
      this.statuses = res.statuses;
      return this.renderTweets();
    })
    .catch(err => {
      this.setSearchDisabled(false);
      console.error(err)
    })
  }
  setSearchDisabled(bool){
    this.searchDisabled = bool;
    $('#search-button').prop('disabled',bool);
  }
  getPosts(q){
    return new Promise((resolve, reject) => {
      $.get('api/posts?q=' + encodeURIComponent(q), data => resolve(data))
      .fail(err => reject(err))
    })
  }
  addLabel(tweetId, label){
    var secret = document.getElementById('secret-input').value
    console.log('Labeling ' + tweetId + ' with ' + label)
    $.ajax({
      type: 'POST',
      url: 'api/label',
      data: JSON.stringify({
        tweetId: tweetId,
        label: label
      }),
      headers: {
        'x-auth-secret': secret
      },
      success: () => {
        console.log('Labeled ' + tweetId + ' ' + label);
      },
      contentType: 'application/json; charset=utf-8',
      dataType: 'json'
    });
  }
  renderTweets(){
    var container = $('#tweet-container');
    var includeRt = $('#include-rt-checkbox').is(':checked');
    var statuses;
    if(!includeRt){
      statuses = this.statuses.filter(status => {
        return status.tweet.text.indexOf('RT') === -1;
      })
    } else {
      statuses = this.statuses;
    }

    container.empty();
    statuses.map(status => {
      var div = document.createElement('div');
      var htmlStr = '';
      div.className = 'tweet-card';
      htmlStr = `
        <div class="card-col-left">
          <img class="twitter-profile-picture" src="${status.tweet.user.profile_image_url}">
        </div>
        <div class="card-col-middle">
          <div>
            <a class="twitter-screenname" href="https://twitter.com/${status.tweet.user.screen_name}" target="_blank">
              ${status.tweet.user.screen_name}
            </a>
            <br>
            ${status.tweet.text}
          </div>
          <div class="metadata-container">
            <span class="metadata-item">Score: ${Math.floor(status.sentiment.compound * 100)/100}</span>
      `
      if(status.prediction){
        htmlStr += `
              <span class="metadata-item">Prediction: ${JSON.stringify(status.prediction.Prediction.predictedScores)}</span>
        `
      }
      htmlStr += `
            <span class="metadata-item">Sentiment: ${Math.floor(status.sentiment.compound * 100)/100}</span>
            <span class="metadata-item">Retweets: ${status.tweet.retweet_count}</span>
            <span class="metadata-item">Favorites: ${status.tweet.favorite_count}</span>
          </div>
        </div>
        <div class="card-col-right">
          <a href="#" onclick="controller.addLabel('${status.tweet.id_str}', 'good')">Good</a>
          <a href="#" onclick="controller.addLabel('${status.tweet.id_str}', 'bad')">Bad</a>
        </div>
      `;
      div.innerHTML = htmlStr;
      container.append(div);
    })
  }
}
