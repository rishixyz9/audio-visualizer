import { exec } from "child_process";

const videoUrl =
  "https://www.youtube.com/watch?v=w4ThD_cxOKQ&ab_channel=DavidDeanBurkhart";
const command = `yt-dlp -f bestaudio --extract-audio --audio-format wav -o "audio.wav" "${videoUrl}"`;

exec(command, (error, stdout, stderr) => {
  if (error) {
    console.error(`Error: ${error.message}`);
    return;
  }
  if (stderr) {
    console.error(`Stderr: ${stderr}`);
  }
  console.log(`Stdout: ${stdout}`);
});
