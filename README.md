# Homebrew tap for macOS apps

This repository is a shared Homebrew tap for macOS apps published under the `kwong` GitHub account.

Users install apps from this tap with:

```bash
brew tap kwong/tap
brew install --cask <app>
```

Examples:

```bash
brew install --cask audx
brew install --cask my-other-app
```

## Repository name

Create the GitHub repository as:

`kwong/homebrew-tap`

Homebrew maps that repository to the short tap name:

`kwong/tap`

## Create a new tap

To create a new personal tap under the `kwong` GitHub account:

1. Create a GitHub repository named `kwong/homebrew-<tap-name>`
2. Clone it locally
3. Create a `Casks/` directory in the repo
4. Add at least one cask file such as `Casks/my-app.rb`
5. Commit and push the repository to GitHub
6. Test it locally with:

```bash
brew untap kwong/<tap-name>
brew tap kwong/<tap-name>
brew install --cask <app>
```

Homebrew maps `kwong/homebrew-<tap-name>` to the short tap name `kwong/<tap-name>`.

For this repository specifically, the concrete values are:

- GitHub repo: `kwong/homebrew-tap`
- Tap name: `kwong/tap`

## How the tap is organized

Each app gets its own cask file in `Casks/`:

- `Casks/audx.rb`
- `Casks/my-other-app.rb`

Each cask should define:

- the app version
- the SHA-256 checksum for the release asset
- the download URL for that app's GitHub release asset
- app metadata such as name, description, and homepage
- the install stanza for that app, such as `app` for app bundles in `.zip` or `.dmg` assets, or `pkg` for installer packages
- cleanup paths in `zap`, plus `uninstall` rules when the app is installed by a `.pkg`

The file `Casks/audx.rb.template` is an example template that can be copied and adapted for other apps.

## Release flow for an app

For each app release:

1. Build the macOS release asset, for example `my-app-1.2.3.dmg`, `my-app-1.2.3-macos.zip`, or `my-app-1.2.3.pkg`
2. Calculate its checksum:

```bash
shasum -a 256 dist/my-app-1.2.3.dmg
```

3. Create or update the app's cask in `Casks/<app>.rb`
4. Set the cask `version` to the app version, for example `1.2.3`
5. Set the cask `sha256` to the first field from the `shasum` output
6. Set the cask `url` to the matching GitHub release asset URL
7. Use the correct install stanza for the asset type:

```ruby
app "My App.app"
```

or:

```ruby
pkg "my-app-1.2.3.pkg"
```

8. If the app installs via `.pkg`, add an `uninstall` section with the app's `pkgutil` id
9. Commit and push this tap repo

## Example cask URL pattern

If an app is released from `kwong/my-app` with tag `v1.2.3` and asset `my-app-1.2.3.dmg`, the cask URL would look like:

```ruby
url "https://github.com/kwong/my-app/releases/download/v#{version}/my-app-#{version}.dmg"
```

## audx example

`audx` now ships both `.dmg` and `.pkg` assets in `v0.1.2`, and this tap targets the DMG so Homebrew installs the app bundle directly.

The live `audx` cask should follow this shape:

```ruby
version "0.1.2"
sha256 "bcd8a8e6384f0baef5ae8c33b2b752df0cf3abcd1e9f7ebec9573dcf5cef8af2"
url "https://github.com/kwong/audx/releases/download/v#{version}/audx-#{version}.dmg"

app "audx.app"
```

`v0.1.2` currently publishes both:

- `audx-<version>.pkg`
- `audx-<version>.dmg`

## First publish checklist

For a new app:

1. Create a GitHub release in the app repository tagged like `v1.2.3`
2. Upload the macOS release asset for that release, such as a `.dmg`, `.zip`, or `.pkg`
3. Add `Casks/<app>.rb` to this repo
4. Verify the cask `version`, `sha256`, and `url` match the uploaded asset exactly
5. Verify the install stanza matches the asset type: `app` for app bundles in `.zip` or `.dmg`, `pkg` for `.pkg`
6. If the app uses `.pkg`, verify the `uninstall pkgutil:` identifier is correct
7. Push this repo to `kwong/homebrew-tap`
8. Test the install:

```bash
brew untap kwong/tap
brew tap kwong/tap
brew install --cask <app>
```

## Notes

- Homebrew installs real cask files such as `Casks/audx.rb`; it does not install directly from a template file.
- A single tap repo can host as many app casks as you want.
- Each app still needs its own cask file because version, checksum, URL, metadata, installer type, and cleanup paths are app-specific.
