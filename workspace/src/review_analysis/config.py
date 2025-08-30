policy_keywords = {
    "spam": [
        "buy now", "click here", "www.", "free voucher", "order now",
        "subscribe", "limited time offer", "promotion code", "get it today"
    ],
    "advertisement": [
        "check our page", "follow us", "shop now", "official website",
        "promo", "special offer", "commercial"
    ],
    "non_visitor": [
        "never been", "heard about", "not visited", "someone told me",
        "read online", "saw on internet"
    ],
    "off_topic": [
        "traffic", "parking", "travel experience", "weather",
        "location not accessible"
    ],
    "rant": [
        "hate", "ruined my day", "personal issues", "friend problems"
    ]
}

policy_scores = {
    "spam": -2,
    "advertisement": -1.5,
    "non_visitor": -2,
    "off_topic": -1,
    "rant": -1
}