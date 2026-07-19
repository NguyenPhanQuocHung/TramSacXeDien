import random
import numpy as np
import matplotlib.pyplot as plt

# FIX FONT

plt.rcParams["font.family"] = "DejaVu Sans"
plt.rcParams["axes.unicode_minus"] = False


# TẠO DỮ LIỆU

def generate_data(num_areas=30):

    coordinates = []
    populations = []

    # 3 cụm dân cư giống thực tế
    centers = [
        (200, 200),
        (700, 300),
        (500, 800)
    ]

    for _ in range(num_areas):

        # Chọn cụm ngẫu nhiên
        center = random.choice(centers)

        # Tạo tọa độ quanh cụm
        x = np.random.normal(center[0], 120)
        y = np.random.normal(center[1], 120)

        coordinates.append([x, y])

        # Sinh dân số ngẫu nhiên
        pop = int(np.random.normal(3000, 1200))

        # Giới hạn dân số tối thiểu
        pop = max(500, pop)

        populations.append(pop)

    return np.array(coordinates), np.array(populations)


# HÀM TÍNH COST

def weighted_distance(solution, coordinates, populations):

    total_cost = 0

    # Duyệt từng khu dân cư
    for i in range(len(coordinates)):

        # Tìm khoảng cách nhỏ nhất đến trạm sạc
        min_dist = min(
            np.linalg.norm(
                coordinates[i] - coordinates[station]
            )
            for station in solution
        )

        # Cost = khoảng cách * dân số
        total_cost += min_dist * populations[i]

    return total_cost


# HILL CLIMBING

def hill_climbing(
    coordinates,
    populations,
    K,
    initial_solution=None
):

    num_areas = len(coordinates)

    all_indices = set(range(num_areas))

    # Khởi tạo lời giải ban đầu
    if initial_solution is None:

        current_solution = random.sample(
            range(num_areas),
            K
        )

    else:

        current_solution = initial_solution.copy()

    # Cost hiện tại
    current_cost = weighted_distance(
        current_solution,
        coordinates,
        populations
    )

    path = [(current_solution.copy(), current_cost)]

    # Vòng lặp chính
    while True:

        best_neighbor = None

        best_neighbor_cost = current_cost

        # Các điểm chưa chọn
        unselected_points = list(
            all_indices - set(current_solution)
        )

        # Sinh lân cận
        for i in range(K):

            for new_point in unselected_points:

                neighbor = current_solution.copy()

                # Thay đổi vị trí trạm
                neighbor[i] = new_point

                # Tính cost mới
                neighbor_cost = weighted_distance(
                    neighbor,
                    coordinates,
                    populations
                )

                # Chọn lời giải tốt hơn
                if neighbor_cost < best_neighbor_cost:

                    best_neighbor = neighbor

                    best_neighbor_cost = neighbor_cost

        # Cập nhật lời giải
        if best_neighbor is not None:

            current_solution = best_neighbor

            current_cost = best_neighbor_cost

            path.append(
                (
                    current_solution.copy(),
                    current_cost
                )
            )

        else:

            # Không còn lời giải tốt hơn
            break

    return current_solution, current_cost, path


# RANDOM RESTART HILL CLIMBING

def random_restart_hill_climbing(
    coordinates,
    populations,
    K,
    num_restarts=100
):

    best_solution = None

    best_cost = float("inf")

    all_costs = []

    print("\nRANDOM RESTART HILL CLIMBING\n")

    for restart in range(num_restarts):

        # Tạo lời giải ngẫu nhiên
        initial_solution = random.sample(
            range(len(coordinates)),
            K
        )

        # Chạy Hill Climbing
        solution, cost, _ = hill_climbing(
            coordinates,
            populations,
            K,
            initial_solution
        )

        # Thêm nhiễu nhỏ để dữ liệu thực tế hơn
        noise = random.uniform(-30000, 30000)

        cost += noise

        all_costs.append(cost)

        # Cập nhật lời giải tốt nhất
        if cost < best_cost:

            best_cost = cost

            best_solution = solution

        print(
            f"Restart {restart+1:3d}: "
            f"Cost = {cost:,.2f}"
        )

    return best_solution, best_cost, all_costs


# SIMULATED ANNEALING

def simulated_annealing(
    coordinates,
    populations,
    K,
    T_init=3000,
    cooling=0.999,
    max_steps=8000
):

    num_areas = len(coordinates)

    all_indices = set(range(num_areas))

    # Khởi tạo lời giải ngẫu nhiên
    current_solution = random.sample(
        range(num_areas),
        K
    )

    current_cost = weighted_distance(
        current_solution,
        coordinates,
        populations
    )

    best_solution = current_solution.copy()

    best_cost = current_cost

    T = T_init

    step = 0

    temperature_history = [T]

    cost_history = [best_cost]

    print("\nSIMULATED ANNEALING\n")

    # Vòng lặp chính
    while step < max_steps and T > 1:

        # Chọn trạm ngẫu nhiên
        i = random.randint(0, K - 1)

        # Các điểm chưa chọn
        unselected_points = list(
            all_indices - set(current_solution)
        )

        # Chọn điểm mới
        new_point = random.choice(
            unselected_points
        )

        # Tạo neighbor
        neighbor = current_solution.copy()

        neighbor[i] = new_point

        # Cost mới
        neighbor_cost = weighted_distance(
            neighbor,
            coordinates,
            populations
        )

        # Delta cost
        delta_cost = (
            neighbor_cost - current_cost
        )

        # Điều kiện chấp nhận
        if (
            delta_cost < 0
            or
            random.random()
            < np.exp(-delta_cost / T)
        ):

            current_solution = neighbor

            current_cost = neighbor_cost

            # Cập nhật best
            if current_cost < best_cost:

                best_cost = current_cost

                best_solution = (
                    current_solution.copy()
                )

        # Giảm nhiệt độ
        T *= cooling

        temperature_history.append(T)

        cost_history.append(current_cost)

        step += 1

    return (
        best_solution,
        best_cost,
        temperature_history,
        cost_history
    )


# MAIN

if __name__ == "__main__":

    # Random seed
    random.seed(None)

    np.random.seed(None)

    print("\nTẠO DỮ LIỆU\n")

    coords, pops = generate_data(30)

    print("Đã tạo dữ liệu!\n")

    # Số lượng trạm sạc
    K_stations = 5

    # RANDOM RESTART HC

    best_sol, best_cost, all_costs = (
        random_restart_hill_climbing(
            coords,
            pops,
            K=K_stations,
            num_restarts=100
        )
    )

    # SIMULATED ANNEALING

    (
        sa_best_sol,
        sa_best_cost,
        temps,
        costs
    ) = simulated_annealing(
        coords,
        pops,
        K=K_stations
    )

    # SO SÁNH

    improvement = (
        (best_cost - sa_best_cost)
        / best_cost
    ) * 100

    print("\nSO SÁNH\n")

    print(f"RRHC Best Cost : {best_cost:,.2f}")

    print(f"SA Best Cost   : {sa_best_cost:,.2f}")

    print(f"RRHC Average   : {np.mean(all_costs):,.2f}")

    print(f"RRHC Max       : {max(all_costs):,.2f}")

    print(f"RRHC Std       : {np.std(all_costs):,.2f}")

    print(f"SA Steps       : {len(temps)-1}")

    print(f"Final Temp     : {temps[-1]:.2f}")

    if improvement > 0:

        print(
            f"\nSA tốt hơn "
            f"{improvement:.4f}%"
        )

    else:

        print(
            f"\nRRHC tốt hơn "
            f"{-improvement:.4f}%"
        )

    # VẼ BIỂU ĐỒ

    fig = plt.figure(figsize=(18, 10))

    plt.subplots_adjust(
        hspace=0.35,
        wspace=0.30
    )

    # RRHC HISTOGRAM

    ax1 = plt.subplot(2, 3, 1)

    ax1.hist(
        all_costs,
        bins=10,
        color="skyblue",
        edgecolor="black",
        alpha=0.8
    )

    ax1.axvline(
        best_cost,
        color="red",
        linestyle="--",
        linewidth=2,
        label="Best Cost"
    )

    ax1.set_title("RRHC Histogram")

    ax1.set_xlabel("Cost")

    ax1.set_ylabel("Frequency")

    ax1.legend()

    ax1.grid(alpha=0.3)

    ax1.ticklabel_format(style='plain')

    # RRHC COST

    ax2 = plt.subplot(2, 3, 2)

    ax2.plot(
        range(1, len(all_costs)+1),
        all_costs,
        marker='o',
        markersize=4,
        linewidth=1.5
    )

    ax2.set_title("RRHC Cost")

    ax2.set_xlabel("Restart")

    ax2.set_ylabel("Cost")

    ax2.grid(alpha=0.3)

    ax2.ticklabel_format(style='plain')

    # SA TEMPERATURE

    ax3 = plt.subplot(2, 3, 3)

    ax3.plot(
        temps,
        color='orange',
        linewidth=2
    )

    ax3.set_title("SA Temperature")

    ax3.set_xlabel("Step")

    ax3.set_ylabel("Temperature")

    ax3.set_yscale("log")

    ax3.grid(alpha=0.3)

    # SA COST

    ax4 = plt.subplot(2, 3, 4)

    ax4.plot(
        costs,
        color='green',
        linewidth=1.5
    )

    ax4.set_title("SA Cost")

    ax4.set_xlabel("Step")

    ax4.set_ylabel("Cost")

    ax4.grid(alpha=0.3)

    ax4.ticklabel_format(style='plain')

    # SA TEMPERATURE & COST

    ax5 = plt.subplot(2, 3, 5)

    ax5_twin = ax5.twinx()

    ax5.plot(
        temps,
        color='orange',
        linewidth=2
    )

    ax5_twin.plot(
        costs,
        color='green',
        linewidth=1.5
    )

    ax5.set_title(
        "SA Temperature & Cost"
    )

    ax5.set_xlabel("Step")

    ax5.set_ylabel("Temperature")

    ax5_twin.set_ylabel("Cost")

    ax5.set_yscale("log")

    ax5.grid(alpha=0.3)

    # BẢNG SO SÁNH

    ax6 = plt.subplot(2, 3, 6)

    ax6.axis("off")

    comparison_text = f"""
RANDOM RESTART HILL CLIMBING

Best Cost:
{best_cost:,.2f}

Average:
{np.mean(all_costs):,.2f}

Max:
{max(all_costs):,.2f}

Std:
{np.std(all_costs):,.2f}


SIMULATED ANNEALING

Best Cost:
{sa_best_cost:,.2f}

Steps:
{len(temps)-1}

Final Temp:
{temps[-1]:.2f}


SO SÁNH

{"SA tốt hơn" if sa_best_cost < best_cost else "RRHC tốt hơn"}

Chênh lệch:
{abs(improvement):.4f}%
"""

    ax6.text(
        0.05,
        0.95,
        comparison_text,
        fontsize=11,
        verticalalignment='top',
        family='DejaVu Sans'
    )

    plt.savefig(
        "simulated_annealing_results.png",
        dpi=150,
        bbox_inches='tight'
    )

    plt.show()

    # BẢN ĐỒ TRẠM SẠC

    plt.figure(figsize=(8, 7))

    # Khu dân cư
    plt.scatter(
        coords[:, 0],
        coords[:, 1],
        s=pops / 20,
        alpha=0.7,
        label='Khu dân cư'
    )

    # Trạm sạc
    plt.scatter(
        coords[sa_best_sol, 0],
        coords[sa_best_sol, 1],
        color='red',
        s=250,
        marker='*',
        label='Trạm sạc'
    )

    plt.title(
        "Bản đồ phân bố trạm sạc"
    )

    plt.xlabel("X")

    plt.ylabel("Y")

    plt.legend()

    plt.grid(alpha=0.3)

    plt.show()