import FFT from "fft.js";
import fs from "fs";

const chunkSize = 2048;
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
				resolve(new Uint8Array(data.subarray(44)));
			}
		});
	});
}

function mapFFTtoFrequencies(fftOutput, sampleRate, fftSize) {
	const nyquist = sampleRate / 2; // Nyquist frequency
	const freqResolution = sampleRate / fftSize; // Frequency bin spacing
	const numBins = fftSize / 2; // Only positive frequencies

	// Generate frequency array
	const frequencies = Array.from(
		{ length: numBins },
		(_, k) => k * freqResolution
	);

	// Compute magnitudes (amplitude spectrum)
	const amplitudes = fftOutput.slice(0, numBins);

	// Map frequencies to amplitudes
	const spectrum = frequencies.map((freq, index) => ({
		frequency: freq,
		amplitude: amplitudes[index],
	}));

	return spectrum;
}

async function async_fft() {
	const raw_data = await read_wav();
	chunks = chunker(raw_data);
	let processed_chunks = [];
	let chunk_count = 0;

	for (const chunk of chunks) {
		const fft = new FFT(chunkSize);
		let output = fft.createComplexArray();
		fft.realTransform(output, chunk);
		fft.completeSpectrum(output);

		const sampleRate = 44100; // Hz
		const fftSize = output.length * 2; // FFT size is typically double the number of amplitude values

		const spectrum = mapFFTtoFrequencies(output, sampleRate, fftSize);

		processed_chunks.push(spectrum);

		if (processed_chunks.length % 128 === 0) {
			fs.writeFile(
				`./chunks/chunk-${chunk_count}.json`,
				JSON.stringify(processed_chunks),
				(err) => {
					console.log(err);
				}
			);
			processed_chunks = [];
			chunk_count++;
		}
	}

	fs.writeFile(
		`./chunks/chunk-${chunk_count}.json`,
		JSON.stringify(processed_chunks),
		(err) => {
			console.log(err);
		}
	);
	processed_chunks = [];
}

async_fft();
