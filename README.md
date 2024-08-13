# X-Unblocker

Unblock all users on X using archive of account data.

## How to use

1. Go to your account settings on X and request an archive of your data. [https://x.com/settings/your_twitter_data/data](https://x.com/settings/your_twitter_data/data)
2. Download the archive and extract.
3. Copy 'block.js' to the same directory as this script.
4. Run 'unblock.py' and login to your X account.

```bash
python unblock.py
```

## Arguments

### `--delay`
Specifies how long to wait for a page to load if the network is slow: 

- slow (5s)
- normal (2s)
- fast (1s)
- or a number in seconds

Default is normal (2s).
