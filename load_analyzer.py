import csv
from pathlib import Path

import matplotlib.pyplot as plt


# 기존 힘 단위 변환기의 변환값을 재사용한다.
FORCE_CONVERTER = {
    "N": 1,
    "kN": 1000,
    "kgf": 9.80665,
    "gf": 0.00980665,
    "lbf": 4.44822,
}

CSV_FILE = Path(__file__).with_name("load_data.csv")
RESULT_FILE = Path(__file__).with_name("load_result.csv")
AREA_MM2 = 100
REFERENCE_STRESS_MPA = 6
REQUIRED_COLUMNS = ("time_s", "force_N")


def read_load_data(csv_file: Path) -> tuple[list[dict[str, float]], int]:
    """CSV 파일에서 유효한 시간(S)과 하중(N) 데이터만 읽는다."""
    with csv_file.open("r", newline="", encoding="utf-8-sig") as file:
        reader = csv.DictReader(file)

        if reader.fieldnames != list(REQUIRED_COLUMNS):
            raise ValueError(
                f"CSV 열 이름은 {', '.join(REQUIRED_COLUMNS)}이어야 합니다."
            )

        data = []
        excluded_count = 0
        for row_number, row in enumerate(reader, start=2):
            try:
                time_value = row["time_s"].strip()
                force_value = row["force_N"].strip()
                if not time_value or not force_value:
                    raise ValueError
                data.append(
                    {
                        "time_s": float(time_value),
                        "force_N": float(force_value)
                        * FORCE_CONVERTER["N"],
                    }
                )
            except (TypeError, ValueError):
                excluded_count += 1
                invalid_values = []
                for column in REQUIRED_COLUMNS:
                    value = row[column].strip()
                    if not value:
                        invalid_values.append(f"{column}='{value}'")
                    else:
                        try:
                            float(value)
                        except ValueError:
                            invalid_values.append(f"{column}='{value}'")
                print(
                    f"원본 CSV {row_number}행을 제외합니다: "
                    f"문제 값 {', '.join(invalid_values)}"
                )

    if not data:
        raise ValueError("유효한 데이터가 없습니다. 계산을 중단합니다.")

    return data, excluded_count


def add_stress(data: list[dict[str, float]]) -> list[dict[str, float]]:
    """하중 데이터를 복사하고 응력(MPa) 열을 추가한다."""
    return [
        {
            **row,
            "stress_MPa": row["force_N"] / AREA_MM2,
        }
        for row in data
    ]


def save_result(data: list[dict[str, float]], result_file: Path) -> None:
    """응력 열이 추가된 데이터를 결과 CSV 파일로 저장한다."""
    fieldnames = ("time_s", "force_N", "stress_MPa")
    with result_file.open("w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(data)


def save_stress_plot(data: list[dict[str, float]], plot_file: Path) -> None:
    """시간-응력 그래프를 점과 선으로 표시해 PNG 파일로 저장한다."""
    time_s = [row["time_s"] for row in data]
    stress_mpa = [row["stress_MPa"] for row in data]
    maximum_stress = max(data, key=lambda row: row["stress_MPa"])

    plt.figure()
    plt.plot(time_s, stress_mpa, marker="o")
    plt.scatter(
        maximum_stress["time_s"],
        maximum_stress["stress_MPa"],
        color="red",
        zorder=3,
    )
    plt.annotate(
        f"{maximum_stress['stress_MPa']:g} MPa",
        (maximum_stress["time_s"], maximum_stress["stress_MPa"]),
        xytext=(8, 8),
        textcoords="offset points",
    )
    plt.xlabel("Time (s)")
    plt.ylabel("Stress (MPa)")
    plt.tight_layout()
    plt.savefig(plot_file)
    plt.close()


def analyze_load_data(
    data: list[dict[str, float]],
) -> tuple[int, float, float, float, float, int]:
    """기본 통계, 최대 응력, 기준 초과 데이터 수를 반환한다."""
    maximum_load = max(data, key=lambda row: row["force_N"])
    maximum_stress = max(data, key=lambda row: row["stress_MPa"])
    over_reference_count = sum(
        row["stress_MPa"] > REFERENCE_STRESS_MPA for row in data
    )
    return (
        len(data),
        maximum_load["force_N"],
        maximum_load["time_s"],
        maximum_stress["stress_MPa"],
        maximum_stress["time_s"],
        over_reference_count,
    )


def main() -> None:
    try:
        raw_data, excluded_count = read_load_data(CSV_FILE)
    except ValueError as error:
        print(error)
        return

    data = add_stress(raw_data)
    save_result(data, RESULT_FILE)
    save_stress_plot(data, Path(__file__).with_name("stress_plot.png"))
    (
        data_count,
        maximum_force,
        maximum_force_time,
        maximum_stress,
        maximum_stress_time,
        over_reference_count,
    ) = analyze_load_data(data)

    print(f"데이터 개수: {data_count}개")
    print(f"제외한 행 수: {excluded_count}개")
    print(f"유효한 데이터 수: {data_count}개")
    print(f"최대 하중: {maximum_force:g} N")
    print(f"최대 하중 발생 시간: {maximum_force_time:g} S")
    print(f"최대 응력: {maximum_stress:g} MPa")
    print(f"최대 응력 발생 시간: {maximum_stress_time:g} S")
    print(
        f"기준 응력({REFERENCE_STRESS_MPA:g} MPa) 초과 데이터 개수: "
        f"{over_reference_count}개"
    )


if __name__ == "__main__":
    main()
