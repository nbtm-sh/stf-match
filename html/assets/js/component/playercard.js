Vue.component('player-card', {
    template: "<div class=player-card><div class=avatar-container><img id=avatar :src='avatar'> <img id=country :src=\"flag\"></div><div class=userdata-container><div class=username-container><span><b>{{ username }}</b></span><br><span id=country-text>{{ country }}</span></div><div class=rank-container><span><i>#{{ rank }}</i></span></div></div></div>",
    data: {
        username: this.username,
        rank: this.rank,
        country: this.country,
        avatar: this.avatar,
        flag: this.flag
    },
    props: {
        username: String,
        rank: Number,
        country: String,
        avatar: String,
        flag: String
    }
});