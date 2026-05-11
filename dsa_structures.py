class Node:
    """
    Đại diện cho một nút trong Danh sách liên kết đôi (Doubly Linked List).
    """
    def __init__(self, data):
        """Khởi tạo một Node với dữ liệu cho trước."""
        self.data = data
        self.prev = None
        self.next = None

class DoublyLinkedList:
    """
    Cấu trúc dữ liệu Danh sách liên kết đôi tự cài đặt.
    Hỗ trợ thao tác thêm vào đuôi O(1), duyệt thuận và duyệt ngược O(N).
    """
    def __init__(self):
        """Khởi tạo danh sách liên kết đôi rỗng."""
        self.head = None
        self.tail = None
        self.size = 0

    def append(self, data):
        """Thêm một phần tử vào cuối danh sách - O(1)"""
        new_node = Node(data)
        if not self.head:
            self.head = self.tail = new_node
        else:
            self.tail.next = new_node
            new_node.prev = self.tail
            self.tail = new_node
        self.size += 1

    def remove(self, node_to_remove):
        """Xóa một Node trực tiếp khỏi danh sách - O(1) nếu đã biết Node"""
        if not node_to_remove:
            return

        # Nếu là node đầu
        if node_to_remove == self.head:
            self.head = node_to_remove.next
            if self.head:
                self.head.prev = None
            else:
                # Nếu danh sách chỉ có 1 phần tử
                self.tail = None
        # Nếu là node cuối
        elif node_to_remove == self.tail:
            self.tail = node_to_remove.prev
            self.tail.next = None
        # Nằm giữa
        else:
            node_to_remove.prev.next = node_to_remove.next
            node_to_remove.next.prev = node_to_remove.prev
        
        self.size -= 1

    def __iter__(self):
        """Hỗ trợ duyệt mảng bằng vòng lặp for...in theo chiều thuận"""
        current = self.head
        while current:
            yield current.data
            current = current.next

    def reverse_iter(self):
        """Hỗ trợ duyệt mảng từ dưới lên (từ đuôi về đầu)"""
        current = self.tail
        while current:
            yield current.data
            current = current.prev

    def __len__(self):
        """Trả về số lượng phần tử hiện có trong danh sách."""
        return self.size


def merge_sort(arr, key=lambda x: x):
    """
    Thuật toán sắp xếp Trộn (Merge Sort) tự cài đặt.
    Thời gian thực thi: O(N log N)
    
    Args:
        arr (list): Danh sách cần sắp xếp
        key (function): Hàm xác định tiêu chí so sánh (ví dụ lambda x: x[0])
    Returns:
        list: Danh sách đã được sắp xếp
    """
    if len(arr) <= 1:
        return arr
    
    mid = len(arr) // 2
    left = merge_sort(arr[:mid], key=key)
    right = merge_sort(arr[mid:], key=key)
    
    return _merge(left, right, key)

def _merge(left, right, key):
    """
    Hàm trộn hai mảng đã sắp xếp thành một mảng hoàn chỉnh.
    
    Args:
        left (list): Nửa mảng bên trái đã sắp xếp.
        right (list): Nửa mảng bên phải đã sắp xếp.
        key (function): Hàm xác định tiêu chí so sánh.
    Returns:
        list: Mảng mới chứa phần tử của cả left và right đã được sắp xếp.
    """
    result = []
    i = j = 0
    
    while i < len(left) and j < len(right):
        if key(left[i]) <= key(right[j]):
            result.append(left[i])
            i += 1
        else:
            result.append(right[j])
            j += 1
            
    # Thêm các phần tử còn sót lại
    result.extend(left[i:])
    result.extend(right[j:])
    
    return result

def compute_lps_array(pattern):
    """
    Tiền xử lý chuỗi mẫu (pattern) để tạo mảng LPS (Longest Prefix Suffix).
    
    Args:
        pattern (str): Chuỗi cần tìm kiếm.
    Returns:
        list: Mảng LPS.
    """
    length = 0
    lps = [0] * len(pattern)
    i = 1
    
    while i < len(pattern):
        if pattern[i] == pattern[length]:
            length += 1
            lps[i] = length
            i += 1
        else:
            if length != 0:
                length = lps[length - 1]
            else:
                lps[i] = 0
                i += 1
    return lps

def kmp_search(text, pattern):
    """
    Thuật toán so khớp chuỗi KMP (Knuth-Morris-Pratt).
    Độ phức tạp O(N + M).
    
    Args:
        text (str): Chuỗi gốc (ví dụ: tên sách).
        pattern (str): Chuỗi cần tìm (từ khóa).
    Returns:
        bool: True nếu tìm thấy, False nếu không.
    """
    if not pattern:
        return True
    if not text:
        return False
        
    M = len(pattern)
    N = len(text)
    
    lps = compute_lps_array(pattern)
    
    i = 0  # Chỉ số cho text
    j = 0  # Chỉ số cho pattern
    
    while (N - i) >= (M - j):
        if pattern[j] == text[i]:
            j += 1
            i += 1
            
        if j == M:
            return True # Tìm thấy (trong đồ án chỉ cần biết là có tồn tại)
            # Nếu cần tìm tất cả vị trí: j = lps[j - 1]
            
        elif i < N and pattern[j] != text[i]:
            if j != 0:
                j = lps[j - 1]
            else:
                i += 1
    return False
