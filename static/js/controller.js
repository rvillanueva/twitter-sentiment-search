class MainController {
  constructor(){

  }
  init(){
    this.getPosts('@barackObama')
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
      return this.renderTweets(res.statuses);
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
  renderTweets(tweets){
    var container = $('#tweet-container');
    container.empty();
    tweets.map(tweet => {
      var div = document.createElement('div');
      div.className = 'tweet-card';
      div.innerHTML = `
        <div class="card-col-left">
          <img class="twitter-profile-picture" src="${tweet.user.profile_image_url}">
        </div>
        <div class="card-col-middle">
          <strong>${tweet.user.screen_name}</strong>
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
