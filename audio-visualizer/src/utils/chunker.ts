import FFT from "fft.js";
import fs from "fs";

const chunkSize = 4096;
let chunks: Uint8Array<ArrayBufferLike>[] = [];

function chunker(data: Uint8Array): Uint8Array<ArrayBufferLike>[] {
	const chunks = [];
	for (let i = 0; i < data.length; i += chunkSize) {
		chunks.push(data.subarray(i, i + chunkSize));
	}
	return chunks;
}

async function read_wav(): Promise<Uint8Array<ArrayBufferLike>> {
	return new Promise((resolve, reject) => {
		fs.readFile("audio.wav", (err, data) => {
			if (err) {
				reject(err);
			} else {
				resolve(new Uint8Array(data));
			}
		});
	});
}

async function async_fft() {
	const raw_data = await read_wav();
	chunks = chunker(raw_data);
	let processed_chunks = [];

	for (let chunk in chunks.slice(0, 10)) {
		let input = new Array(chunkSize).fill(0).map((_, i) => chunk[i] || 0);
		const fft = new FFT(chunkSize);
		const output = fft.createComplexArray();
		fft.realTransform(output, input);
		fft.completeSpectrum(output);
		processed_chunks.push(output);
	}

	fs.writeFileSync("fft.json", JSON.stringify(processed_chunks));
}

async_fft();
