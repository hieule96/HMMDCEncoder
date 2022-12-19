#include <exception>
// now int the exception on parsing nal unit, after the 


typedef enum BitstreamException
{
    BS_BUFFER_OVERFLOW = 0,
    BS_BUFFER_UNDERFLOW,
    BS_READ_ERROR_OVER_32_BITS,
    BS_READ_BYTE_ALIGN_ERROR,
    BS_OTHER
} BitstreamException;

class BitstreamInputException : public std::exception
{
public:
    BitstreamInputException(BitstreamException exception) : m_exceptionType(exception) {
        switch (m_exceptionType)
        {
        case BS_BUFFER_OVERFLOW:
            m_msg = "[BitstreamInput] Buffer overflow";
            break;
        case BS_BUFFER_UNDERFLOW:
            m_msg = "[BitstreamInput] Buffer underflow";
            break;
        case BS_READ_ERROR_OVER_32_BITS:
            m_msg = "[BitstreamInput] Read error over 32 bits";
            break;
        case BS_READ_BYTE_ALIGN_ERROR:
            m_msg = "[BitstreamInput] Read byte align error";
            break;
        default:
            m_msg = "[BitstreamInput] Unhandle exception";
            break;
        }
    }
    BitstreamException getExceptionType() { return m_exceptionType; }
    virtual const char* what() const throw() { return m_msg; }
private:
    const char* m_msg;
    BitstreamException m_exceptionType;
};