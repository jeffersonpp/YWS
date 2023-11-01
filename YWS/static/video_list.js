class VideoFrame {
    constructor(id) {
        this.id = id;
        this.box = document.getElementById("box_" + this.id);
        this.startTimes();
        this.getVideoDetails();
        this.hide();
    }

    finalize = () => {
        let timer_bg;
        let total = 270;
        let bg_size;
        let partsize = (total / (parseInt(this.duration) * 1000));

        for (let i = 0, size = this.lines.length; i < size; i++) {
            timer_bg = document.createElement("div");
            timer_bg.className = "timer_bg";
            bg_size = (this.lines[i].dataset.start) * partsize;
            timer_bg.style.width = `${parseInt(bg_size)}px`;
            this.lines[i].append(timer_bg)
        }
    }

    show = () => {
        if (!this.player) {
            this.loadVideo();
            for (let l = 0, size = this.lines.length; l < size; l++) {
                this.lines[l].classList.add("blocked");
            }
        }
        this.box.setAttribute("style", "display: inline-block;");
    }

    hide = () => {
        this.box.setAttribute("style", "display: none;");
        if (this.player) {
            this.player.stopVideo();
        }
    }

    setPosition = (pos) => {
        this.parent.style.position = "absolute";
        this.parent.style.left = `${pos.left}px`;
        this.parent.style.top = `${pos.top}px`;
    }

    startTimes = () => {
        this.html_element = document.getElementById(this.id);
        this.parent = this.html_element.parentNode;
        this.lines = this.parent.getElementsByClassName("time_frame");
        for (let i = 0, size = this.lines.length; i < size; i++) {
            this.lines[i].addEventListener("click", this.startPlayerHere);
        }
    }

    startPlayerHere = (e) => {
        let element = e.target;
        if (element.className === "timer_bg") {
            element = element.parentNode;
        }
        if (!element.classList.contains("blocked")) {
            let start = parseInt(element.dataset.start)
            this.playVideoAt(start);
        }
    }

    playVideoAt = (start) => {
        if (this.playerIsReady()) {
            console.log(this.player.getCurrentTime());
            this.player.playVideo();
            let play_at = start / 1000;
            play_at -= 1.25;
            this.player.seekTo(play_at, true);
        } else {
            if (this.reboot) {
                setTimeout(() => {
                    if (typeof this.player.playVideo !== "function") {
                        this.player = null;
                    }
                }, 1000);
            } else {
                this.reboot = true;
                this.loadVideo();
                setTimeout(() => {
                    this.playVideoAt(start);
                }, 500);
            }
        }
    }

    playerIsReady = () => {
        return this.ready && typeof this.player.playVideo === 'function';
    }

    loadVideo = () => {
        window.YT.ready(() => {
            this.player = new YT.Player(this.id, {
                height: '200',
                width: '400',
                videoId: this.id,
                events: {
                    'onReady': this.onPlayerReady
                },
                playerVars: {
                    'autoplay': 0,
                    'cc_load_policy': 1,
                    'controls': 1
                }
            });
        });
    }

    onPlayerReady = (e) => {
        this.ready = true;
        for (let i = 0, size = this.lines.length; i < size; i++) {
            this.lines[i].classList.remove("blocked");
        }
    }

    getVideoDetails = () => {
        const xhr = new XMLHttpRequest();
        xhr.open("POST", "/details", true);
        xhr.setRequestHeader("Content-Type", "application/x-www-form-urlencoded");
        xhr.onreadystatechange = () => {
            if (xhr.readyState === XMLHttpRequest.DONE && xhr.status === 200) {
                let response = JSON.parse(xhr.response)
                this.channel = response.channel;
                this.duration = response.duration;
                this.upload = response.upload;
                this.views = response.views
                setTimeout(() => {
                    this.finalize();
                }, 50);
            }
        };
        xhr.send(`video=${this.id}`);
    }
}

let pointer = {
    page: 1
};
let per_page = 8;
let video_dict = {};
let video_list = [];
let original_list = [];

window.onload = () => {
    let video_frame = document.getElementsByClassName("video_frame");

    for (let video of video_frame) {
        video_list.push(video.id);
        video_dict[video.id] = new VideoFrame(video.id);
    }
    original_list = [...video_list];

    if (video_list.length > 0) {
        let total_pages = document.getElementById("total_pages");
        let page = document.getElementById("page");
        let max_pages = Math.ceil(video_list.length / per_page);
        page.setAttribute("max", max_pages)
        total_pages.innerHTML = max_pages;
        paginate();
    }
}

const changeOrder = (value) => {
    pre_list = []

    if (value === "word") {
        paginate(pointer["page"]);
        list = [...original_list]
    } else {
        for (let i = 0, size = video_list.length; i < size; i++) {
            let current = video_dict[video_list[i]]
            let obj = {
                channel: current.channel,
                duration: parseInt(current.duration),
                date: parseInt(current.upload),
                views: parseInt(current.views),
                video: video_list[i]
            }
            pre_list.push(obj);
        }
        if (value == "date") {
            pre_list = pre_list.sort((a, b) => {
                return a["date"] > b["date"] ? 1 : -1;
            });
        } else if (value == "views") {
            pre_list = pre_list.sort((a, b) => {
                return a["views"] > b["views"] ? 1 : -1;
            });
        } else if (value == "channel") {
            pre_list = pre_list.sort((a, b) => {
                return a["channel"] > b["channel"] ? 1 : -1;
            });
        }

        for (let j = 0, limit = pre_list.length; j < limit; j++) {
            video_list[j] = pre_list[j]["video"];
        }
        console.log("PAGE AT CHANGEORDER", pointer["page"])
        paginate(pointer["page"]);
    }
}

paginate = (page) => {
    if (page) {
        pointer["page"] = page;
    }
    page = parseInt(pointer["page"]);

    console.log("PAGINATE TO PAGE", page)

    let limit = video_list.length;

    if (page >= 1) {
        for (let i = 0; i < limit; i++) {
            current = video_list[i];
            if (video_dict[current]) {
                video_dict[current].hide();
            }
        }
    }

    limit = (page * per_page) > video_list.length ? video_list.length : (page * per_page);


    console.log("PRINT start", ((page - 1) * per_page), "LIMIT", limit);

    for (let index = ((page - 1) * per_page); index < limit; index++) {
        current = video_list[index];
        video_dict[current].show();
    }
}