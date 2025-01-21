import { A } from "@solidjs/router";
import { createSignal, createEffect } from "solid-js";

import * as THREE from "three";
import apply_basic_circle_effect from "~/utils/audio-animations";
import apply_random_noise from "~/utils/random-noise";
import apply_perlin_noise from "~/utils/perlin-noise";

export default function Home() {
	let kick = 0;
	let damping = 0.25;

	let n = 0;

	const socket = new WebSocket("ws://localhost:8000/ws");
	let time = 0;

	socket.onopen = () => {
		time = 0;
		console.log("WebSocket connection established");
	};

	socket.onmessage = (event) => {
		time += 1;

		let data: any;

		try {
			data = JSON.parse(event.data);
			const absSinSumAtT = data[0].reduce(
				(sum: any, f: any, index: any) => {
					const A = data[1][index];
					if (A > 0) {
						sum += Math.abs(
							A * Math.sin(2 * Math.PI * f * (time / 10))
						);
					}
					return sum;
				},
				0
			);

			kick = absSinSumAtT;
		} catch (error) {
			console.log("hi");
		}

		console.log(data);

		console.log("Message from server:", event.data);
	};

	socket.onclose = () => {
		time = 0;
		console.log("WebSocket connection closed");
	};

	socket.onerror = (error) => {
		console.error("WebSocket error:", error);
	};

	createEffect(() => {
		const scene = new THREE.Scene();
		const camera = new THREE.PerspectiveCamera(75, 16 / 9, 0.1, 1000);

		camera.position.set(0, 0, 200);
		camera.lookAt(0, 0, 0);

		let geometry = new THREE.BufferGeometry().setFromPoints(
			new THREE.Path()
				.absarc(0, 0, 50, 0, Math.PI * 2)
				.getSpacedPoints(360)
		);

		let material = new THREE.LineBasicMaterial({ color: "aqua" });
		let line = new THREE.Line(geometry, material);
		scene.add(line);

		const renderer = new THREE.WebGLRenderer();
		renderer.setSize(800, 450);
		renderer.domElement.style.margin = "0 auto";
		renderer.domElement.style.border = "1px solid white";
		renderer.domElement.style.borderRadius = "5px";
		document.body.appendChild(renderer.domElement);

		renderer.render(scene, camera);

		function animate() {
			requestAnimationFrame(animate);

			const positions = geometry.attributes.position.array;

			let min_length = 50 + kick * 0.25;
			let max_length = 50 + kick * 1.5;
			let scale = Math.min(0.05 * kick, 10);
			let smoothing = Math.max(5, kick * 0.4);

			switch (n) {
				case 0:
					apply_basic_circle_effect(
						positions,
						kick,
						min_length,
						max_length,
						damping
					);
					break;
				case 1:
					apply_random_noise(
						positions,
						min_length,
						max_length,
						0.1 * kick,
						damping
					);
					break;
				case 2:
					apply_perlin_noise(
						positions,
						min_length,
						max_length,
						kick,
						smoothing,
						damping
					);
					break;
			}

			geometry.attributes.position.needsUpdate = true;

			renderer.render(scene, camera);
		}
		animate();
		return () => {
			document.body.removeChild(renderer.domElement);
		};
	}, kick);

	function play() {
		socket.send("play");
	}

	function pause() {
		socket.send("pause");
		kick = 0;
	}

	function stop() {
		socket.send("stop");
		kick = 0;
	}

	return (
		<div class="container mx-auto">
			<div class="text-center mx-auto text-gray-700 p-4">home</div>

			<div class="flex flex-row justify-between w-1/2 mx-auto mb-2">
				<a
					on:click={play}
					class="border-[#00f8f9] text-gray-300 p-4 pt-2 pb-2 rounded-sm bg-[#00f8f9]/50 h-8 w-24 text-center hover:cursor-pointer"
				>
					play
				</a>
				<a
					on:click={pause}
					class="border-[#00f8f9] text-gray-300 p-4 pt-2 pb-2 rounded-sm bg-[#00f8f9]/50 h-8 w-24 text-center hover:cursor-pointer"
				>
					pause
				</a>
				<a
					on:click={stop}
					class="border-[#00f8f9] text-gray-300 p-4 pt-2 pb-2 rounded-sm bg-[#00f8f9]/50 h-8 w-24 text-center hover:cursor-pointer"
				>
					stop
				</a>

				<select
					class="border-[#00f8f9] text-gray-300 p-4 pt-2 pb-2 rounded-sm bg-[#00f8f9]/50 h-8 w-24 text-center hover:cursor-pointer"
					onChange={(e) => {
						n = e.currentTarget.selectedIndex;
					}}
				>
					<option>circle</option>
					<option>random</option>
					<option>perlin</option>
				</select>

				<input
					type="range"
					min="0.05"
					max="1"
					step="0.05"
					class="border-[#00f8f9] text-gray-300 rounded-sm bg-[#00f8f9]/50 h-8 w-24 hover:cursor-pointer"
					onInput={(e) => {
						damping = parseFloat(e.currentTarget.value);
						// Use the damping value as needed in your animation logic
					}}
				/>
			</div>
		</div>
	);
}
