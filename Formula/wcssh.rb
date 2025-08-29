class Wcssh < Formula
  desc "A Warp-native multi-SSH launcher that opens a new window, splits panes, and enables synchronized input by default."
  homepage "https://github.com/waynelloyd/homebrew-wcssh"
  url "https://github.com/waynelloyd/homebrew-wcssh/archive/refs/tags/v0.1.0.tar.gz"
  sha256 "8c6ee10c56287d597095781ce770b5e8df3f6c36f2affe28b283db3bd423a805" # Replace this with the output of: shasum -a 256 v0.1.0.tar.gz
  license "MIT"

  def install
    bin.install "wcssh.py" => "wcssh"
  end

  test do
    system "#{bin}/wcssh", "--version"
  end
end
