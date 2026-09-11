from library import AlreadyBorrowedError, BookNotFoundError, DuplicatedISBNError, Library
lib = Library()

# 테스트 편의용 더미데이터
lib.create_paper_book("1001", "파이썬 기초", "김철수", "A구역 1번")
lib.create_paper_book("1002", "객체지향의 사실과 오해", "조영호", "B구역 3번")
lib.create_E_book("2001", "클린 코드", "Robert C. Martin", "PDF", 15)
lib.create_E_book("2002", "이펙티브 파이썬", "Brett Slatkin", "EPUB", 8)
lib.create_E_book("2003", "파이썬 데이터 분석", "김철수", "EPUB", 12)

print("도서관에 오신걸 환영합니다.")
while True:
    print("메뉴목록")
    print("[1] 모든 도서 목록 조회")
    print("[2] 모든 저자 조회")
    print("[3] 도서 제목 또는 저자로 검색")
    print("[4] 도서 등록")
    print("[5] 도서 대출")
    print("[6] 도서 반납")
    print("[7] 도서 삭제")
    print("[0] 끝내기")

    text = input("번호를 입력해주세요: ")
    
    if not text.isdigit():
        print("숫자만 입력해주세요.")
        continue
        
    num = int(text)

    # 모든 도서 목록 조회
    if num == 1:
        books = lib.show_all_books()
        if books:
            print("등록된 도서 목록 : ")
            for book in books:
                print(book)
        else:
            print("등록된 도서가 없습니다.")

    # 모든 저자 조회
    elif num == 2:
        authors = lib.show_all_authors()
        if authors:
            print("등록된 저자 목록 : ")
            for author in authors:
                print(author)
        else:
            print("등록된 도서가 없습니다.")

    # 도서 제목 또는 저자로 검색
    elif num == 3:
        while True:
            search_input = input("도서 제목으로 검색하실거면 [1], 저자로 검색하실거면 [2]를 눌러주세요: ")
            if not search_input.isdigit():
                print("숫자만 입력해주세요.")
                continue
            search_input_num = int(search_input)

            # 제목으로 검색
            if search_input_num == 1:
                title = input("도서 제목으로 검색할 키워드를 입력해주세요: ")
                print("검색결과")
                books = lib.search_book(title=title)
                if books:
                    for book in books:
                        print(book)
                else:
                    print("검색결과가 없습니다.")
                break
            # 저자로 검색
            elif search_input_num == 2:
                author = input("저자 이름으로 검색할 키워드를 입력해주세요: ")
                print("검색결과")
                books = lib.search_book(author=author)
                if books:
                    for book in books:
                        print(book)
                else:
                    print("검색결과가 없습니다.")
                break
            else:
                print("유효하지 않은 숫자입니다.")

    # 도서 등록
    elif num == 4:
        while True:
            type_input = input("일반 도서 등록은 [1], 전자책 등록은 [2]를 눌러주세요: \n 메인으로 돌아가시려면 [0]을 입력해주세요: ")
            if not type_input.isdigit():
                print("숫자만 입력해주세요.")
                continue
            
            type_num = int(type_input)
            if type_num not in (1, 2, 0):
                print("유효하지 않은 번호입니다.")
                continue

            if type_num == 0:
                break

            isbn = input("ISBN: ")
            title = input("도서 제목: ")
            author = input("저자: ")
            
            try:
                if type_num == 1:
                    location = input("소장 위치: ")
                    book = lib.create_paper_book(isbn, title, author, location)
                    print(f"'{book.title}' 일반 도서가 등록되었습니다.")
                elif type_num == 2:
                    file_format = input("파일 형식 (예: PDF, EPUB): ")
                    size_input = input("파일 크기(MB): ")
                    if not size_input.isdigit():
                        print("파일 크기는 숫자만 입력해주세요. 등록이 취소됩니다.")
                        break
                    file_size_mb = int(size_input)
                    
                    book = lib.create_E_book(isbn, title, author, file_format, file_size_mb)
                    print(f"'{book.title}' 전자책이 등록되었습니다.")
                break
            except DuplicatedISBNError as e:
                print(e)
                break

    # 도서 대출
    elif num == 5:
        isbn_input = input("대출할 도서의 ISBN을 입력해주세요: ")
        try:
            book = lib.borrow(isbn_input)
            print(f"{book.title} 도서의 대출이 성공적으로 처리되었습니다.")
        except BookNotFoundError as e:
            print(e)
        except AlreadyBorrowedError as e:
            print(e)



    # 도서 반납
    elif num == 6:
        isbn_input = input("반납할 도서의 ISBN을 입력해주세요: ")
        try:
            book = lib.return_book(isbn_input)
            if book:
                print(f"{book.title} 도서의 반납이 성공적으로 처리되었습니다.")
            else:
                print("해당 도서는 현재 대출중인 도서가 아닙니다.")
        except BookNotFoundError as e:
            print(e)

    # 도서 삭제
    elif num == 7:
        isbn_input = input("삭제할 도서의 ISBN을 입력해주세요: ")
        try:
            book = lib.delete_book(isbn_input)
            print(f"{book.title} 도서의 삭제가 성공적으로 처리되었습니다.")
        except BookNotFoundError as e:
            print(e)
    
    elif num == 0:
        print("프로그램을 종료합니다.")
        break

    else:
        print("유효하지 않은 숫자입니다.")