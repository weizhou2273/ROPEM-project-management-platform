$(document).ready(function() {
    TweenLite.set("#atAd300x600", {visibility:"visible"});
    var tl, frame2, frame3;

    
    frame2 = new SplitText('#frame2', {type: "words", wordsClass:"word++"});
    frame3 = new SplitText('#frame3', {type: "words", wordsClass:"word++"});
    


    CSSPlugin.useSVGTransformAttr = true


    tl = new TimelineMax();

    tl.to("#flash", 0, {opacity:0, left:1000})    
    
    tl.staggerFrom(frame2.words, 0.2, {left: -300}, 0.07)

    tl.to("#frame2", 0.3, {autoAlpha: 0, delay:2});

    tl.to("#bgImg2", 0.5, {left:0});

    tl.staggerFrom(frame3.words, 0.2, {left: -300}, 0.07)
	
	tl.to("#bkgReveal", 0.3, {autoAlpha: 1, delay: 2});	
	
	tl.to(".fade", 0.3, {autoAlpha: 1});
	
	tl.to(".fade1", 1, {autoAlpha: 1});
	
	tl.to("#Allstate", 0.3, {bottom:37})
	
    tl.to("#btn_cta", 0.3, {right:1}); 

});



var div1 = $("div#btn_cta"),
    tn1 = TweenMax.to(div1, .3, {
        right: -12,
        repeat: -1,
        yoyo: true,
        ease: Linear.easeNone,
        paused: true
    });

div1.mouseenter(function() {
    tn1.play();
});

div1.mouseleave(function() {
    var currentTime = tn1.time();
    tn1.reverse(currentTime);
});