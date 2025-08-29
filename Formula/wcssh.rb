class Wcssh < Formula
  desc "A Warp-native multi-SSH launcher that opens a new window, splits panes, and enables synchronized input by default."
  homepage "https://github.com/waynelloyd/homebrew-wcssh"
  url "https://github.com/waynelloyd/homebrew-wcssh/archive/refs/tags/v1.0.0.tar.gz"
  sha256 "3b6b9c3d0db2b96a8494e8cf67e2c931e53f1cf1734950a61e58bfdd8d70c59c" # Replace this with the output of: shasum -a 256 v0.1.0.tar.gz
  license "MIT"

  def install
    bin.install "wcssh.py" => "wcssh"
  end

  test do
    system "#{bin}/wcssh", "--version"
  end
end
