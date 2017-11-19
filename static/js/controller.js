class MainController {
  constructor(){
    this.statuses = [];
    this.labelIndex = {};
    this.advancedMode = false;
  }
  init(){
    this.addEventListeners();
  }
  addEventListeners(){
    $('#include-rt-checkbox').change(() => {
      this.renderTweets();
    });
    $('#secret-input').on('input', () => {
      if(!this.advancedMode){
        this.advancedMode = true;
        this.renderTweets();
      }
    })
  }
  search(input){
    var term = input || $('#search-input').val();
    if(!term){
      console.error('No search term provided.')
      return;
    }
    console.log('Searching for ' + term);
    this.setSearchDisabled(true);
    this.tweets = [];
    this.renderTweets();
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
    var secret = document.getElementById('secret-input').value
    return new Promise((resolve, reject) => {
      $.ajax({
        type: 'GET',
        url: 'api/posts?q=' + encodeURIComponent(q),
        headers: {
          'x-auth-secret': secret
        },
        success: data => {
          resolve(data);
        },
        fail: err => {
          reject(err)
        }
      });
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
    this.labelIndex[tweetId] = label;
    this.renderTweets();
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
            <a
              class="metadata-item"
              href="https://twitter.com/${status.tweet.user.screen_name}/status/${status.tweet.id_str}"
              target="_blank"
            >View Tweet</a>
            <span class="metadata-item">Score: ${Math.floor(status.score * 100)/100}</span>
      `
      if(status['ml_prediction']){
        var mlScore;
        if(status['ml_prediction'].Prediction.predictedLabel === '0'){
          mlScore = 1 - status['ml_prediction'].Prediction.predictedScores['0']
        } else {
          mlScore = status['ml_prediction'].Prediction.predictedScores['1']
        }
        htmlStr += `
              <span class="metadata-item">Prediction: ${Math.floor(mlScore * 100)/100}</span>
        `
      }
      htmlStr += `
            <span class="metadata-item">Sentiment: ${Math.floor(status.sentiment.compound * 100)/100}</span>
            <span class="metadata-item">Retweets: ${status.tweet.retweet_count}</span>
            <span class="metadata-item">Favorites: ${status.tweet.favorite_count}</span>
          </div>
        </div>
      `;
      if(this.advancedMode){
          htmlStr += `
            <div class="card-col-right">
          `
          if(this.labelIndex[status.tweet.id_str] === 1){
            htmlStr += `
                Keep
            `
          } else {
            htmlStr += `
                <button href="#" onclick="controller.addLabel('${status.tweet.id_str}', 1)">Keep</button>
            `
          }
          if(this.labelIndex[status.tweet.id_str] === 0){
            htmlStr += `
                Remove
            `
          } else {
            htmlStr += `
                <button href="#" onclick="controller.addLabel('${status.tweet.id_str}', 0)">Remove<buttona>
            `
          }
          htmlStr += `
            </div>
          `
      }
      div.innerHTML = htmlStr;
      container.append(div);
    })
  }
}
