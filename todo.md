Just a place to organize my thoughts for now. In the future I should probably
use issues for these and start managing this as a real project :D

- [ ] Features:
    - [ ] event pub/sub (presently only a stub exists)
    - [ ] integrate logging (possibly using pub/sub as a hook)
    - [ ] function result checking method - enable customization via argument also
    - [ ] exception checking method - enable customization via argument also
    - [ ] ++ statistics for retries

- [ ] Testing:
    - [ ] event pub/sub
    - [ ] callable args
    - [ ] dynamically following module defaults (if not overridden by arg)
    - [ ] dynamically following arg changes (when callable used)
    - [ ] what other features aren't covered well?

- [ ] Documentation:
    - [ ] ++ more examples into readme (basically the advert set of examples)
    - [ ] recipes? (more detailed examples illustrating more features

- [ ] Extensions:
    - [ ] backoff sub-module: + jitter
    - [ ] updates to 'simple' sub-module? determine what features it will/won't get
    - [ ] specify 'policy', use for one or more uses of retry
    - [ ] thread safety? cross thread reporting/stats/etc?

