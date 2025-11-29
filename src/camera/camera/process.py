import rclpy
from rclpy.node import Node
from sensor_msgs.msg import Image
import cv2
from cv_bridge import CvBridge

class ImageProcessor(Node):
    def __init__(self):
        super().__init__('image_processor')
        self.subscription = self.create_subscription(
            Image,
            '/rgb',
            self.listener_callback,
            10)
        self.publisher = self.create_publisher(Image, '/camera', 10)
        self.bridge = CvBridge()
        self.count = 0

    def listener_callback(self, msg):
        # Convert ROS Image message to OpenCV image
        cv_image = self.bridge.imgmsg_to_cv2(msg, desired_encoding='bgr8')

        # Process the image (e.g., convert to grayscale)
        gray_image = cv2.cvtColor(cv_image, cv2.COLOR_BGR2GRAY)

        # Convert back to ROS Image message
        processed_msg = self.bridge.cv2_to_imgmsg(gray_image, encoding='mono8')

        if self.count < 5:
            # Save image to disk
            filename = f'/tmp/processed_image_{self.count}.png'
            cv2.imwrite(filename, gray_image)
            self.count += 1
            self.get_logger().info(f'Saved {filename}')

        # Publish the processed image
        self.publisher.publish(processed_msg)

def main(args=None):
    rclpy.init(args=args)
    image_processor = ImageProcessor()
    rclpy.spin(image_processor)
    image_processor.destroy_node()
    rclpy.shutdown()

if __name__ == '__main__':
    main()