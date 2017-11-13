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
    console.log('Searching for ' + input);
    this.setSearchDisabled(true);
    this.getPosts(term)
    .then(res => {
      this.setSearchDisabled(false);
      console.log(res);
      this.tweets = res.statuses;
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
  renderTweets(){
    var container = $('#tweet-container');
    var includeRt = $('#include-rt-checkbox').is(':checked');
    var tweets;
    if(!includeRt){
      tweets = this.tweets.filter(tweet => {
        return tweet.text.indexOf('RT') === -1;
      })
    } else {
      tweets = this.tweets;
    }

    container.empty();
    tweets.map(tweet => {
      var div = document.createElement('div');
      div.className = 'tweet-card';
      div.innerHTML = `
        <div class="card-col-left">
          <img class="twitter-profile-picture" src="${tweet.user.profile_image_url}">
        </div>
        <div class="card-col-middle">
          <a class="twitter-screenname" href="https://twitter.com/${tweet.user.screen_name}" target="_blank">
            ${tweet.user.screen_name}
          </a>
          <br>
          ${tweet.text}
        </div>
        <div class="card-col-right">
          Sentiment: ${Math.floor(tweet.sentiment.compound * 100)/100}
          <br>
        </div>
      `;
      container.append(div);
    })
  }
}
