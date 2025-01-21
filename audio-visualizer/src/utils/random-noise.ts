import * as THREE from "three";

export default function apply_random_noise(
	positions: THREE.TypedArray,
	min_length: number,
	max_length: number,
	scale?: number,
	damping?: number
) {
	scale = scale || 1;
	damping = damping || 0.25;

	for (let i = 0; i < positions.length; i += 3) {
		let noise = (Math.random() - 0.5) * scale;

		let a = positions[i];
		let b = positions[i + 1];
		let theta = Math.atan2(b, a);

		let r = Math.sqrt(a * a + b * b);

		let new_length = Math.min(Math.max(min_length, r + noise), max_length);

		const position_vec3 = new THREE.Vector3(
			positions[i],
			positions[i + 1],
			1
		);

		const targetPosition = new THREE.Vector3(
			new_length * Math.cos(theta),
			new_length * Math.sin(theta),
			1
		);

		const newPosition = position_vec3.lerp(targetPosition, damping);

		positions[i] = newPosition.x;
		positions[i + 1] = newPosition.y;
	}

	return positions;
}
