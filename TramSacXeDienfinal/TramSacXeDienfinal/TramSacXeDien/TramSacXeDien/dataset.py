import random
import numpy as np
import matplotlib.pyplot as plt

# =====================================================
# TẠO DỮ LIỆU NGẪU NHIÊN
# =====================================================

def generate_data(num_areas=30):

    # Tạo tọa độ ngẫu nhiên dạng float
    coordinates = np.random.uniform(
        0,
        1000,
        size=(num_areas, 2)
    )

    # Tạo dân số ngẫu nhiên
    populations = np.random.randint(
        100,
        5000,
        size=num_areas
    )

    return coordinates, populations


# =====================================================
# HÀM TÍNH CHI PHÍ
# =====================================================

def weighted_distance(solution, coordinates, populations):

    total_cost = 0

    # Duyệt từng khu dân cư
    for i in range(len(coordinates)):

        # Tìm khoảng cách gần nhất
        min_dist = min(
            np.linalg.norm(
                coordinates[i] - coordinates[station]
            )
            for station in solution
        )

        # Cost = khoảng cách × dân số
        total_cost += min_dist * populations[i]

    return total_cost


# =====================================================
# HILL CLIMBING
# =====================================================

def hill_climbing(
    coordinates,
    populations,
    K,
    initial_solution=None
):

    num_areas = len(coordinates)

    # Tập tất cả vị trí
    all_indices = set(range(num_areas))

    # =================================================
    # KHỞI TẠO NGẪU NHIÊN
    # =================================================

    if initial_solution is None:

        current_solution = random.sample(
            range(num_areas),
            K
        )

    else:

        current_solution = initial_solution.copy()

    # Tính cost ban đầu
    current_cost = weighted_distance(
        current_solution,
        coordinates,
        populations
    )

    # Lưu đường đi
    path = [(current_solution.copy(), current_cost)]

    iteration = 1

    verbose = initial_solution is None

    # =================================================
    # VÒNG LẶP CHÍNH
    # =================================================

    while True:

        best_neighbor = None

        best_neighbor_cost = current_cost

        # Các điểm chưa được chọn
        unselected_points = list(
            all_indices - set(current_solution)
        )

        # =================================================
        # SINH LÂN CẬN
        # =================================================

        for i in range(K):

            for new_point in unselected_points:

                # Copy solution hiện tại
                neighbor = current_solution.copy()

                # Thay 1 trạm bằng điểm mới
                neighbor[i] = new_point

                # Tính cost mới
                neighbor_cost = weighted_distance(
                    neighbor,
                    coordinates,
                    populations
                )

                # Thêm nhiễu random nhỏ
                neighbor_cost += random.uniform(0, 50)

                # Nếu tốt hơn
                if neighbor_cost < best_neighbor_cost:

                    best_neighbor = neighbor

                    best_neighbor_cost = neighbor_cost

        # =================================================
        # QUYẾT ĐỊNH DI CHUYỂN
        # =================================================

        if best_neighbor is not None:

            # Cập nhật lời giải
            current_solution = best_neighbor

            current_cost = best_neighbor_cost

            # Lưu path
            path.append(
                (
                    current_solution.copy(),
                    current_cost
                )
            )

            if verbose:

                print(
                    f"Bước {iteration}: "
                    f"Cost = {current_cost:,.2f}"
                )

            iteration += 1

        else:

            if verbose:

                print(
                    "-> Không tìm được "
                    "lân cận tốt hơn"
                )

                print("-> Đạt Local Optima!")

            break

    return current_solution, current_cost, path


# =====================================================
# RANDOM RESTART HILL CLIMBING
# =====================================================

def random_restart_hill_climbing(
    coordinates,
    populations,
    K,
    num_restarts=100,
    verbose=True
):

    num_areas = len(coordinates)

    best_solution = None

    best_cost = float('inf')

    all_costs = []

    if verbose:
        print("\n===================================")
        print(" RANDOM RESTART HILL CLIMBING ")
        print("===================================")

    # Chạy nhiều lần
    for restart in range(num_restarts):

        # Tạo random solution
        initial_solution = random.sample(
            range(num_areas),
            K
        )

        # Chạy Hill Climbing
        solution, cost, _ = hill_climbing(
            coordinates,
            populations,
            K,
            initial_solution
        )

        # Lưu cost
        all_costs.append(cost)

        # Cập nhật best
        if cost < best_cost:

            best_cost = cost

            best_solution = solution

        if verbose:
            print(
                f"Restart {restart+1:3d}: "
                f"Cost = {cost:>15,.2f}"
            )

    return best_solution, best_cost, all_costs


# =====================================================
# SIMULATED ANNEALING
# =====================================================

def simulated_annealing(
    coordinates,
    populations,
    K,
    T_init=10000,
    cooling=0.997,
    max_steps=15000,
    verbose=True
):

    num_areas = len(coordinates)

    # Tập vị trí
    all_indices = set(range(num_areas))

    # Khởi tạo ngẫu nhiên
    current_solution = random.sample(
        range(num_areas),
        K
    )

    # Cost ban đầu
    current_cost = weighted_distance(
        current_solution,
        coordinates,
        populations
    )

    # Best solution
    best_solution = current_solution.copy()

    best_cost = current_cost

    # Nhiệt độ ban đầu
    T = T_init

    step = 0

    # Lưu lịch sử
    temperature_history = [T]

    cost_history = [best_cost]

    if verbose:
        print("\n===================================")
        print(" SIMULATED ANNEALING ")
        print("===================================")

        print(f"T_init   = {T_init}")

        print(f"Cooling  = {cooling}")

        print(f"Max Step = {max_steps}")

    # =================================================
    # VÒNG LẶP CHÍNH
    # =================================================

    while step < max_steps and T > 1.0:

        # Chọn ngẫu nhiên 1 trạm
        i = random.randint(0, K - 1)

        # Các điểm chưa được chọn
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

        # Tính cost mới
        neighbor_cost = weighted_distance(
            neighbor,
            coordinates,
            populations
        )

        # Delta cost
        delta_cost = (
            neighbor_cost - current_cost
        )

        # =================================================
        # ĐIỀU KIỆN CHẤP NHẬN
        # =================================================

        if (
            delta_cost < 0
            or
            random.random()
            < np.exp(-delta_cost / T)
        ):

            current_solution = neighbor

            current_cost = neighbor_cost

            # Update best
            if current_cost < best_cost:

                best_cost = current_cost

                best_solution = (
                    current_solution.copy()
                )

        # Giảm nhiệt độ
        T = T * cooling

        # Lưu lịch sử
        temperature_history.append(T)

        cost_history.append(best_cost)

        step += 1

        # In mỗi 1000 bước
        if verbose and step % 1000 == 0:

            print(
                f"Step {step:5d} | "
                f"T = {T:10.2f} | "
                f"Best Cost = {best_cost:,.2f}"
            )

    if verbose:
        print("\nHoàn thành Simulated Annealing!")

        print(f"Best Cost = {best_cost:,.2f}")

    return (
        best_solution,
        best_cost,
        temperature_history,
        cost_history
    )


# =====================================================
# MAIN
# =====================================================

if __name__ == "__main__":

    # =================================================
    # RANDOM SEED NGẪU NHIÊN
    # =================================================

    random.seed(None)

    np.random.seed(None)

    print("===================================")
    print(" TẠO DỮ LIỆU NGẪU NHIÊN ")
    print("===================================")

    # Tạo dữ liệu
    coords, pops = generate_data(
        num_areas=30
    )

    print("Đã tạo dữ liệu!")

    # Số lượng trạm sạc
    K_stations = 5

    # =================================================
    # RANDOM RESTART HILL CLIMBING
    # =================================================

    best_sol, best_cost, all_costs = (
        random_restart_hill_climbing(
            coords,
            pops,
            K=K_stations,
            num_restarts=100
        )
    )

    # =================================================
    # SIMULATED ANNEALING
    # =================================================

    (
        sa_best_sol,
        sa_best_cost,
        temps,
        costs
    ) = simulated_annealing(
        coords,
        pops,
        K=K_stations,
        T_init=10000,
        cooling=0.997,
        max_steps=15000
    )

    # =================================================
    # KẾT QUẢ
    # =================================================

    print("\n===================================")
    print(" RANDOM RESTART RESULT ")
    print("===================================")

    print("Best Solution:", best_sol)

    print(f"Best Cost: {best_cost:,.2f}")

    print(
        f"Average Cost: "
        f"{np.mean(all_costs):,.2f}"
    )

    print("\n===================================")
    print(" SIMULATED ANNEALING RESULT ")
    print("===================================")

    print("Best Solution:", sa_best_sol)

    print(
        f"Best Cost: "
        f"{sa_best_cost:,.2f}"
    )

    print(
        f"Final Temperature: "
        f"{temps[-1]:.2f}"
    )

    # =================================================
    # SO SÁNH
    # =================================================

    improvement = (
        (best_cost - sa_best_cost)
        / best_cost
    ) * 100

    print("\n===================================")
    print(" COMPARISON ")
    print("===================================")

    print(f"RRHC = {best_cost:,.2f}")

    print(f"SA   = {sa_best_cost:,.2f}")

    if improvement > 0:

        print(
            f"SA tốt hơn "
            f"{improvement:.2f}%"
        )

    else:

        print(
            f"RRHC tốt hơn "
            f"{-improvement:.2f}%"
        )

    # =================================================
    # BIỂU ĐỒ
    # =================================================

    fig = plt.figure(figsize=(16, 10))

    # =================================================
    # 1. HISTOGRAM RRHC
    # =================================================

    ax1 = plt.subplot(2, 3, 1)

    ax1.hist(
        all_costs,
        bins=20,
        color='skyblue',
        edgecolor='black'
    )

    ax1.axvline(
        best_cost,
        color='red',
        linestyle='--',
        linewidth=2
    )

    ax1.set_title("RRHC Histogram")

    ax1.set_xlabel("Cost")

    ax1.set_ylabel("Frequency")

    # =================================================
    # 2. COST THEO RESTART
    # =================================================

    ax2 = plt.subplot(2, 3, 2)

    ax2.plot(
        range(1, len(all_costs)+1),
        all_costs,
        marker='o',
        linewidth=1
    )

    ax2.set_title("RRHC Cost")

    ax2.set_xlabel("Restart")

    ax2.set_ylabel("Cost")

    ax2.grid(alpha=0.3)

    # =================================================
    # 3. NHIỆT ĐỘ SA
    # =================================================

    ax3 = plt.subplot(2, 3, 3)

    ax3.plot(
        temps,
        color='orange'
    )

    ax3.set_title("SA Temperature")

    ax3.set_xlabel("Step")

    ax3.set_ylabel("Temperature")

    ax3.set_yscale('log')

    ax3.grid(alpha=0.3)

    # =================================================
    # 4. COST SA
    # =================================================

    ax4 = plt.subplot(2, 3, 4)

    ax4.plot(
        costs,
        color='green'
    )

    ax4.set_title("SA Best Cost")

    ax4.set_xlabel("Step")

    ax4.set_ylabel("Best Cost")

    ax4.grid(alpha=0.3)

    # =================================================
    # 5. DUAL AXIS
    # =================================================

    ax5 = plt.subplot(2, 3, 5)

    ax5_twin = ax5.twinx()

    ax5.plot(
        temps,
        color='orange'
    )

    ax5_twin.plot(
        costs,
        color='green'
    )

    ax5.set_title(
        "SA Temperature & Cost"
    )

    ax5.set_xlabel("Step")

    ax5.set_ylabel("Temperature")

    ax5_twin.set_ylabel("Best Cost")

    ax5.set_yscale('log')

    # =================================================
    # 6. BẢNG KẾT QUẢ
    # =================================================

    ax6 = plt.subplot(2, 3, 6)

    ax6.axis('off')

    comparison_text = f"""
RANDOM RESTART HILL CLIMBING

Best Cost :
{best_cost:,.2f}

Average :
{np.mean(all_costs):,.2f}

Max :
{max(all_costs):,.2f}

Std :
{np.std(all_costs):,.2f}

SIMULATED ANNEALING

Best Cost :
{sa_best_cost:,.2f}

Steps :
{len(temps)-1}

Final Temp :
{temps[-1]:.2f}

Kết luận:
{"SA tốt hơn" if sa_best_cost < best_cost else "RRHC tốt hơn"}
"""

    ax6.text(
        0.1,
        0.5,
        comparison_text,
        fontsize=10,
        family='monospace'
    )

    plt.tight_layout()

    # Lưu hình
    plt.savefig(
        "simulated_annealing_results.png",
        dpi=150
    )

    print("\nĐã lưu file:")
    print("simulated_annealing_results.png")

    plt.show()

    # =================================================
    # BẢN ĐỒ PHÂN BỐ
    # =================================================

    plt.figure(figsize=(7, 6))

    # Khu dân cư
    plt.scatter(
        coords[:, 0],
        coords[:, 1],
        s=pops / 20,
        alpha=0.6,
        label='Khu dân cư'
    )

    # Trạm sạc
    plt.scatter(
        coords[sa_best_sol, 0],
        coords[sa_best_sol, 1],
        color='red',
        s=200,
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