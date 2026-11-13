// Low-poly Nissan Leaf visualization built from primitive markers
// (visualization_msgs/MarkerArray, max 20 markers).
// Dimensions are measured from meshes/Nissan_Leaf_Simulation_02_06.obj,
// origin = rear axle center (nissan9/base_link), x forward, z up.

#include <chrono>
#include <cmath>
#include <string>

#include "rclcpp/rclcpp.hpp"
#include "visualization_msgs/msg/marker_array.hpp"

using namespace std::chrono_literals;
using visualization_msgs::msg::Marker;
using visualization_msgs::msg::MarkerArray;

namespace
{
struct Rgba
{
    float r, g, b, a;
};

const Rgba kBody{0.95f, 0.95f, 0.95f, 1.0f};
const Rgba kPlastic{0.08f, 0.08f, 0.08f, 1.0f};
const Rgba kGlass{0.07f, 0.06f, 0.13f, 0.95f};
const Rgba kTire{0.20f, 0.20f, 0.20f, 1.0f};
const Rgba kRim{0.62f, 0.62f, 0.62f, 1.0f};
const Rgba kHeadlight{0.69f, 0.71f, 0.95f, 1.0f};
const Rgba kTaillight{0.90f, 0.05f, 0.05f, 1.0f};
const Rgba kSensorBar{0.12f, 0.0f, 1.0f, 1.0f};
const Rgba kAntenna{0.80f, 0.80f, 0.80f, 1.0f};

constexpr double kWheelBase = 2.73;
constexpr double kWheelY = 0.76;
constexpr double kWheelRadius = 0.33;
}  // namespace

class NissanMarkerPublisher : public rclcpp::Node
{
public:
    NissanMarkerPublisher() : Node("nissan_marker_publisher")
    {
        frame_id_ = this->declare_parameter<std::string>("frame_id", "nissan9/base_link");
        const auto topic = this->declare_parameter<std::string>("topic", "nissan_marker");
        const auto rate = this->declare_parameter<double>("publish_rate", 1.0);

        // Transient local: late-joining subscribers with the same QoS get the model at once.
        // Periodic republish covers volatile subscribers (RViz default).
        pub_ = this->create_publisher<MarkerArray>(topic, rclcpp::QoS(1).transient_local());
        build();
        pub_->publish(markers_);
        timer_ = this->create_wall_timer(
            std::chrono::duration<double>(1.0 / std::max(rate, 0.01)),
            [this]() { pub_->publish(markers_); });

        RCLCPP_INFO_STREAM(this->get_logger(), "Publishing " << markers_.markers.size()
                           << " markers on '" << topic << "' in frame '" << frame_id_ << "'");
    }

private:
    // Rotation about the y axis (pitch), positive = nose down for +x.
    static geometry_msgs::msg::Quaternion pitch(double deg)
    {
        const double h = deg * M_PI / 360.0;
        geometry_msgs::msg::Quaternion q;
        q.y = std::sin(h);
        q.w = std::cos(h);
        return q;
    }

    // Cylinder axis rotated from z to y (wheel axle direction).
    static geometry_msgs::msg::Quaternion axleY()
    {
        geometry_msgs::msg::Quaternion q;
        q.x = M_SQRT1_2;
        q.w = M_SQRT1_2;
        return q;
    }

    Marker & add(int type, double x, double y, double z,
                 double sx, double sy, double sz, const Rgba & c,
                 const geometry_msgs::msg::Quaternion & q = geometry_msgs::msg::Quaternion())
    {
        Marker m;
        m.header.frame_id = frame_id_;
        // stamp left at 0 -> RViz/Foxglove use the latest available TF
        m.ns = "nissan_body";
        m.id = static_cast<int>(markers_.markers.size());
        m.type = type;
        m.action = Marker::ADD;
        m.frame_locked = true;
        m.pose.position.x = x;
        m.pose.position.y = y;
        m.pose.position.z = z;
        m.pose.orientation = q;
        m.scale.x = sx;
        m.scale.y = sy;
        m.scale.z = sz;
        m.color.r = c.r;
        m.color.g = c.g;
        m.color.b = c.b;
        m.color.a = c.a;
        markers_.markers.push_back(m);
        return markers_.markers.back();
    }

    void build()
    {
        markers_.markers.clear();

        // --- Body (8 markers) ---
        add(Marker::CUBE, 1.485, 0.0, 0.20, 4.47, 1.76, 0.60, kBody);               // lower body
        add(Marker::CUBE, 0.94, 0.0, 0.63, 3.32, 1.76, 0.26, kBody);                // shoulder / belt line
        add(Marker::CUBE, 3.11, 0.0, 0.513, 1.21, 1.72, 0.20, kBody, pitch(14.4));  // sloped hood
        add(Marker::CUBE, 0.75, 0.0, 0.92, 2.30, 1.52, 0.36, kGlass);               // side windows / cabin
        add(Marker::CUBE, 0.75, 0.0, 1.145, 2.20, 1.42, 0.13, kBody);               // roof
        add(Marker::CUBE, 2.205, 0.0, 0.885, 0.84, 1.50, 0.10, kGlass, pitch(24.4)); // windshield
        add(Marker::CUBE, -0.52, 0.0, 0.925, 0.45, 1.45, 0.08, kGlass, pitch(-49.7)); // rear window
        add(Marker::CUBE, 1.49, 0.0, -0.04, 4.54, 1.80, 0.18, kPlastic);            // bumpers / side skirt

        // --- Wheels: tire + rim (8 markers) ---
        for (double x : {0.0, kWheelBase}) {
            for (double s : {1.0, -1.0}) {
                add(Marker::CYLINDER, x, s * kWheelY, 0.0,
                    2 * kWheelRadius, 2 * kWheelRadius, 0.22, kTire, axleY());
                add(Marker::CYLINDER, x, s * (kWheelY + 0.005), 0.0,
                    0.40, 0.40, 0.225, kRim, axleY());
            }
        }

        // --- Lights (1 CUBE_LIST marker, per-point colors) ---
        auto & lights = add(Marker::CUBE_LIST, 0.0, 0.0, 0.0, 0.35, 0.14, 0.10, kBody);
        const struct { double x, y, z; Rgba c; } lamp_pts[] = {
            {3.00, 0.64, 0.62, kHeadlight}, {3.00, -0.64, 0.62, kHeadlight},
            {-0.66, 0.62, 0.62, kTaillight}, {-0.66, -0.62, 0.62, kTaillight},
        };
        for (const auto & l : lamp_pts) {
            geometry_msgs::msg::Point p;
            p.x = l.x;
            p.y = l.y;
            p.z = l.z;
            lights.points.push_back(p);
            std_msgs::msg::ColorRGBA c;
            c.r = l.c.r;
            c.g = l.c.g;
            c.b = l.c.b;
            c.a = l.c.a;
            lights.colors.push_back(c);
        }

        // --- Roof sensors (3 markers) ---
        add(Marker::CUBE, 1.755, 0.0, 1.195, 0.11, 1.48, 0.19, kSensorBar);         // sensor crossbar
        add(Marker::CYLINDER, -0.20, 0.0, 1.17, 0.15, 0.15, 0.06, kAntenna);        // rear GNSS antenna
        add(Marker::CYLINDER, 1.85, -0.06, 1.285, 0.18, 0.18, 0.04, kAntenna);      // front GNSS antenna
    }

    std::string frame_id_;
    MarkerArray markers_;
    rclcpp::Publisher<MarkerArray>::SharedPtr pub_;
    rclcpp::TimerBase::SharedPtr timer_;
};

int main(int argc, char ** argv)
{
    rclcpp::init(argc, argv);
    rclcpp::spin(std::make_shared<NissanMarkerPublisher>());
    rclcpp::shutdown();
    return 0;
}
