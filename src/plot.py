import matplotlib.pyplot as plt
plt.figure(figsize=(3.5, 2.5))

tellers = [3, 4, 5]
wq_simulation = [3.202, 0.539, 0.135]
wq_theory = [3.236, 0.538, 0.131]

plt.plot(tellers, wq_simulation, marker="o", label="Simulation")
plt.plot(tellers, wq_theory, marker="s", linestyle="--", label="Theory")
plt.xticks(tellers)
plt.xlabel("Number of tellers")
plt.ylabel("Average waiting time (min)")
plt.legend()
plt.tight_layout()
plt.savefig("figures/waiting_time.png", dpi=300)
plt.show()