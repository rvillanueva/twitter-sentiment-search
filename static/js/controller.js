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
    this.getPosts(term)
    .then(res => {
      console.log(res);
      return this.renderTweets(res.statuses);
    })
    .catch(err => console.error(err))
  }
  getPosts(q){
    return new Promise((resolve, reject) => {
      $.get('api/posts?q=' + encodeURIComponent(q), data => resolve(data))
      .fail(err => reject(err))
    })
  }
  renderTweets(tweets){
    var container = $('#tweet-container');
    tweets.map(tweet => {
      var div = document.createElement('div');
      div.className = 'tweet-card';
      div.innerHTML = `
        <img src="${tweet.user.profile_image_url}">
        <strong>${tweet.user.screen_name}</strong>
        <br>
        ${tweet.text}
      `;
      container.append(div);
    })
  }
}
