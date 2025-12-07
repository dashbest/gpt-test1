(() => {
  const hands = ["グー", "チョキ", "パー"];
  const handHints = "グー/チョキ/パー または rock/scissors/paper";

  const normalizeHand = (raw) => {
    if (!raw) return null;
    const value = raw.trim().toLowerCase();
    switch (value) {
      case "グー":
      case "ぐー":
      case "g":
      case "rock":
        return "グー";
      case "チョキ":
      case "ちょき":
      case "c":
      case "scissors":
        return "チョキ";
      case "パー":
      case "ぱー":
      case "p":
      case "paper":
        return "パー";
      default:
        return null;
    }
  };

  const judge = (player, cpu) => {
    if (player === cpu) return "draw";
    const winPairs = {
      "グー": "チョキ",
      "チョキ": "パー",
      "パー": "グー",
    };
    return winPairs[player] === cpu ? "win" : "lose";
  };

  const messages = {
    win: "あなたの勝ち！🎉",
    lose: "残念、コンピュータの勝ち！",
    draw: "あいこでした。もう一回！",
  };

  const summarize = (score) =>
    `これまでの結果: ${score.win}勝 ${score.lose}敗 ${score.draw}分`;

  window.playJanken = function playJanken() {
    const score = { win: 0, lose: 0, draw: 0 };

    while (true) {
      const input = prompt(`じゃんけん！ ${handHints}\n(キャンセルすると終了します)`);
      if (input === null) {
        console.log("ゲームを終了します。");
        break;
      }

      const playerHand = normalizeHand(input);
      if (!playerHand) {
        console.warn(`入力を理解できませんでした。${handHints} を試してください。`);
        continue;
      }

      const cpuHand = hands[Math.floor(Math.random() * hands.length)];
      const result = judge(playerHand, cpuHand);
      score[result] += 1;

      console.log(`あなた: ${playerHand} / コンピュータ: ${cpuHand}`);
      console.log(messages[result]);
      console.log(summarize(score));

      const again = confirm("もう一度プレイしますか？");
      if (!again) {
        console.log("遊んでくれてありがとう！");
        break;
      }
    }
  };

  console.log("playJanken() を実行するとじゃんけんを開始できます。");
})();
